from ast import literal_eval
from collections import namedtuple
import re
from django.db.models import ForeignKey
import Results.models
from ScenarioCreator.models import Zone, ProductionType


def camel_case_spaces(name_with_spaces):
    return re.sub(r' (\w)', lambda match: match.group(1).upper(), name_with_spaces)


class DailyParser():
    possible_zones = {x.name for x in Zone.objects.all()}.union({'Background'})
    possible_pts = {x.name for x in ProductionType.objects.all()}.union({''})
    failures = set()

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
                pref_all = prefix.replace('All', '')
                if pref_all not in road_map:
                    road_map[pref_all] = prefix  # special case where C removes All when suffixed by a Production Type

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
            for column_name, model_field in field_map.items():
                if suffix_key == '' and model_class_name == 'DailyByProductionType' \
                        and column_name in 'deswU deswA expnU expcU expnA expcA infnU infcU infnA infcA'.split():
                    column_name = column_name + "All"  # sometimes columns use "All" instead of ''
                if column_name + suffix_key in sparse_info:
                    setattr(instance, model_field, sparse_info[column_name + suffix_key])
                    try:
                        self.failures.remove(column_name + suffix_key)
                    except KeyError:
                        print('Error: Column was assigned twice.  Second copy in %s.%s for output column %s.' % (model_class_name, model_field, column_name + suffix_key))

            instance_dict[suffix_key].save()


    def construct_combinatorial_instances(self, day, iteration):
        daily_instances = {table_name:{} for table_name in ["DailyByProductionType", "DailyByZone", "DailyByZoneAndProductionType", "DailyControls"]}

        daily_by_pt = daily_instances["DailyByProductionType"]
        for pt_name in self.possible_pts:
            pt = ProductionType.objects.filter(name=pt_name).first()  # obj or None
            daily_by_pt[camel_case_spaces(pt_name)] = \
                Results.models.DailyByProductionType(production_type=pt, iteration=iteration, day=day)

        daily_instances["DailyByZone"] = {camel_case_spaces(zone_name):
            Results.models.DailyByZone(zone=Zone.objects.filter(name=zone_name).first(), iteration=iteration, day=day) for zone_name in self.possible_zones}

        daily_by_pt_zone = daily_instances["DailyByZoneAndProductionType"]
        for pt_name in self.possible_pts:
            pt = ProductionType.objects.filter(name=pt_name).first()
            for zone_name in self.possible_zones:
                zone = Zone.objects.filter(name=zone_name).first()
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

        for class_name in daily_instances:
            self.populate_tables_with_matching_fields(class_name, daily_instances[class_name], sparse_info)  # there was a lot of preamble to get this line to work

        if len(self.failures):
            print('Unable to match columns: ', sorted(self.failures))
        else:
            print("Done parsing Day", day, "Iteration", iteration)


