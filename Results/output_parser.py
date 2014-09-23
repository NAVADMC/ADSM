from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.builtins import int
from future.builtins import zip
from future.builtins import str
from future import standard_library
standard_library.install_hooks()
from future.builtins import object
from ast import literal_eval
from collections import namedtuple
import re
import Results.models
from ScenarioCreator.models import Zone, ProductionType


def camel_case_spaces(name_with_spaces):
    return re.sub(r' (\w)', lambda match: match.group(1).upper(), name_with_spaces)


def number(string):
    try:
        return int(string)
    except:
        try:
            return float(string)
        except:
            return -1


class DailyParser(object):
    def __init__(self, header_line):
        self.headers = header_line.strip().split(',')  # there was a trailing /r/n to remove
        self.possible_zones = {x.name for x in Zone.objects.all()}.union({'Background'})
        self.possible_pts = {x.name for x in ProductionType.objects.all()}.union({''})
        self.failures = set()


    def extract_name(self, c_header_name, possibilities):
        """Returns the header with the name clipped out and the matching name if it is in the list of possibilities.
         Use for extracting zone and production type names from CEngine output."""
        for name in possibilities:
            if self.camel_case_spaces(name) in c_header_name:  # It's important to camelCase this to match C output
                shortened = re.sub(self.camel_case_spaces(name), '', c_header_name)
                return shortened, name
        return c_header_name, None

    def build_composite_field_map(self, table):
        road_map = {}
        for prefix, field in table:
            if prefix not in ('iteration', 'day', 'production_type', 'zone'):  # skip the selector fields
                road_map[prefix] = prefix

        return road_map

    def stripped_field(self, c_header_name):
        c_header_name, zone = self.extract_name(c_header_name, self.possible_zones)
        c_header_name, pt = self.extract_name(c_header_name, self.possible_pts)
        return c_header_name

    def populate_tables_with_matching_fields(self, model_class_name, instance_dict, sparse_info):
        """Populates all combinations of a particular table in one go.  This method must be called once for each
        model class that you want populated.
        model_class_name: named of table defined in Results.models
        instance_dict: a dictionary containing one instance of every combination of parameters.  Keys are the "suffix" e.g. _Bull_HighRisk
        sparse_info: Dictionary containing all the key, value pairs that the simulation put out
        field_map: Keys are all column names to match to (prefix only), values are exact field name in that model.  The distinction allows
            the program to map multiple columns onto the same field.  There are some special cases where column name is not exactly field + suffix.
        """
        field_map = self.build_composite_field_map(getattr(Results.models, model_class_name)() )  # creates a table instance
        for suffix_key, instance in instance_dict.items():  # For each combination: DailyByZoneAndProductionType with (Bull_HighRisk), (Swine_MediumRisk), etc.
            instance_needed = False
            for column_name, model_field in field_map.items():
                if column_name + suffix_key in sparse_info:
                    setattr(instance, model_field, sparse_info[column_name + suffix_key])
                    instance_needed = True
                    try:
                        self.failures.remove(column_name + suffix_key)
                    except KeyError:
                        print('Error: Column was assigned twice.  Second copy in %s.%s for output column %s.' % (model_class_name, model_field, column_name + suffix_key))
            if not instance_needed:
                del instance_dict[suffix_key]
        return [instance for key, instance in instance_dict.items()]

    def construct_combinatorial_instances(self, day, iteration):
        """This constructs a mapping between the name of the column 'suffix' for example: 'BackgroundCattle' and maps it
        to the appropriate Django query settings to grab the matching model instance.  For 'BackgroundCattle' the query
        should be `DailyByZoneAndProductionType(production_type__name=Cattle, zone=None, ...`.
        This handles the special blank case for both "All ProductionType" = '' and "Background Zone" = None.
        
        It returns a dict which is the collection of all the model instances which will need to be populated each day:
        1 DailyControls
        1*pt DailyByProductionType
        zones*pt DailyByZoneAndProductionType
        zones*1 DailyByZone
        """
        daily_instances = {table_name:{} for table_name in ["DailyByProductionType", "DailyByZone", "DailyByZoneAndProductionType", "DailyControls"]}

        daily_by_pt = daily_instances["DailyByProductionType"]
        for pt_name in self.possible_pts:
            pt = ProductionType.objects.filter(name=pt_name).first()  # obj or None for "All Animals" case
            daily_by_pt[camel_case_spaces(pt_name)] = \
                Results.models.DailyByProductionType(production_type=pt, iteration=iteration, day=day)

        daily_instances["DailyByZone"] = {camel_case_spaces(zone_name):
            Results.models.DailyByZone(zone=Zone.objects.filter(name=zone_name).first(), iteration=iteration, day=day) for zone_name in self.possible_zones}

        daily_by_pt_zone = daily_instances["DailyByZoneAndProductionType"]
        for pt_name in self.possible_pts:
            pt = ProductionType.objects.filter(name=pt_name).first()  # obj or None for "All Animals" case
            for zone_name in self.possible_zones:
                zone = Zone.objects.filter(name=zone_name).first()  # obj or None for "Background" case
                daily_by_pt_zone[camel_case_spaces(zone_name + pt_name)] = \
                    Results.models.DailyByZoneAndProductionType(production_type=pt, zone=zone, iteration=iteration, day=day)

        daily_instances["DailyControls"] = {'': Results.models.DailyControls(iteration=iteration, day=day)}  # there's only one of these
        return daily_instances


    def populate_db_from_daily_report(self, sparse_info):
        """Parses the C Engine stdout and populates the appropriate models with the information.  Takes one line
        at a time, representing one DailyReport."""
        assert isinstance(sparse_info, dict)
        # sparse_info = literal_eval(report.sparse_dict)
        # print(sparse_info)
        iteration = sparse_info['Run']
        del sparse_info['Run']
        day = sparse_info['Day']
        del sparse_info['Day']

        self.failures = set(sparse_info.keys())  # whatever is left is a failure

        #construct the set of tables we're going to use for this day
        daily_instances = self.construct_combinatorial_instances(day, iteration)

        results = []
        for class_name in daily_instances:
            result = self.populate_tables_with_matching_fields(class_name, daily_instances[class_name], sparse_info)  # there was a lot of preamble to get this line to work
            results.extend(result)

        if len(self.failures) and day == 1:
            print('Unable to match columns: ', len(self.failures), sorted(self.failures))
        return results


    def parse_daily_strings(self, cmd_strings):
        results = []
        for cmd_string in cmd_strings:
            values = cmd_string.split(',')
            if len(values):
                pairs = zip(self.headers, values)
                sparse_values = {a: number(b) for a, b in pairs}
                Results.models.DailyReport(sparse_dict=str(sparse_values), full_line=cmd_string).save()
                results.extend(self.populate_db_from_daily_report(sparse_values))
        return results
