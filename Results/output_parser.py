import re
from django.db import connections
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


def build_composite_field_map( table):
    road_map = {}
    for prefix, field in table:
        if prefix not in ('iteration', 'day', 'production_type', 'zone'):  # skip the selector fields
            road_map[prefix] = prefix

    return road_map


class DailyParser(object):
    def __init__(self, header_line, production_types, zones):
        self.production_types = production_types
        self.zones = zones
        self.headers = header_line.strip().split(',')  # there was a trailing /r/n to remove
        self.possible_zones = {x[1] for x in zones}.union({'Background'})
        self.possible_pts = {x[1] for x in production_types}.union({''})
        self.failures = set()

    def populate_tables_with_matching_fields(self, model_class_name, instance_dict, sparse_info):
        """Populates all combinations of a particular table in one go.  This method must be called once for each
        model class that you want populated.
        model_class_name: named of table defined in Results.models
        instance_dict: a dictionary containing one instance of every combination of parameters.  Keys are the "suffix" e.g. _Bull_HighRisk
        sparse_info: Dictionary containing all the key, value pairs that the simulation put out
        field_map: Keys are all column names to match to (prefix only), values are exact field name in that model.  The distinction allows
            the program to map multiple columns onto the same field.  There are some special cases where column name is not exactly field + suffix.
        """
        field_map = build_composite_field_map(getattr(Results.models, model_class_name)() )  # creates a table instance
        keys_to_delete = []
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
                else:
                    pass  # It's okay for the model to specify a field that the C Engine doesn't output.  No harm done
            if not instance_needed:
                keys_to_delete.append(suffix_key)
        for suffix_key in keys_to_delete:
            del instance_dict[suffix_key] 
        return [instance for key, instance in instance_dict.items()]

    def construct_combinatorial_instances(self, day, iteration, last_line):
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
            try:
                pt = [x[0] for x in self.production_types if x[1] == pt_name][0]
            except IndexError:
                pt = None
            daily_by_pt[camel_case_spaces(pt_name)] = \
                Results.models.DailyByProductionType(production_type_id=pt, iteration=iteration, day=day, last_day=last_line)

        daily_instances["DailyByZone"] = {}
        for zone_name in self.possible_zones:
            try:
                zone = [x[0] for x in self.zones if x[1] == zone_name][0]
            except IndexError:
                zone = None
            instance = Results.models.DailyByZone(zone_id=zone, iteration=iteration, day=day, last_day=last_line)
            daily_instances["DailyByZone"][camel_case_spaces(zone_name)] = instance

        daily_by_pt_zone = daily_instances["DailyByZoneAndProductionType"]
        for pt_name in self.possible_pts:
            try:
                pt = [x[0] for x in self.production_types if x[1] == pt_name][0]
            except IndexError:
                pt = None
            for zone_name in self.possible_zones:
                try:
                    zone = [x[0] for x in self.zones if x[1] == zone_name][0]
                except IndexError:
                    zone = None
                daily_by_pt_zone[camel_case_spaces(zone_name + pt_name)] = \
                    Results.models.DailyByZoneAndProductionType(production_type_id=pt, zone_id=zone, iteration=iteration, day=day, last_day=last_line)

        daily_instances["DailyControls"] = {'': Results.models.DailyControls(iteration=iteration, day=day, last_day=last_line)}  # there's only one of these
        return daily_instances

    def populate_db_from_daily_report(self, sparse_info, last_line):
        """Parses the C Engine stdout and populates the appropriate models with the information.  Takes one line
        at a time, representing one DailyReport."""
        assert isinstance(sparse_info, dict)
        # sparse_info = literal_eval(report.sparse_dict)
        # print(sparse_info)
        try:
            iteration = sparse_info['Run']
            del sparse_info['Run']
            day = sparse_info['Day']
            del sparse_info['Day']
            del sparse_info['versionMajor']
            del sparse_info['versionMinor']
            del sparse_info['versionRelease']
            if last_line:
                print("Finished Iteration %i:  %i Days" % (iteration, day))
        except:
            return []
        self.failures = set(sparse_info.keys())  # whatever is left is a failure

        #construct the set of tables we're going to use for this day
        daily_instances = self.construct_combinatorial_instances(day, iteration, last_line)

        results = []
        for class_name in daily_instances:
            result = self.populate_tables_with_matching_fields(class_name, daily_instances[class_name], sparse_info)  # there was a lot of preamble to get this line to work
            results.extend(result)

        if len(self.failures) and day == 1:
            print('Unable to match columns: ', len(self.failures), sorted(self.failures))
        return results

    def parse_daily_strings(self, cmd_string, last_line=False, create_version_entry=False):
        results = []
        if cmd_string:
            values = cmd_string.split(',')
            if len(values):
                pairs = zip(self.headers, values)
                sparse_values = {a: number(b) for a, b in pairs}
                if create_version_entry:
                    version = Results.models.ResultsVersion()
                    version.versionMajor = sparse_values['versionMajor']
                    version.versionMinor = sparse_values['versionMinor']
                    version.versionRelease = sparse_values['versionRelease']
                    results.extend([version])
                    create_version_entry = False  # only run once
                results.extend(self.populate_db_from_daily_report(sparse_values, last_line))
        return results

    def parse_unit_stats_string(self, cmd_string):
        values = cmd_string.split(',')
        if len(values) == 5 and (values[1] or values[2] or values[3] or values[4]):
            try:
                unit = values[0]
                WAS_INFECTED, WAS_ZONE_FOCUS, WAS_VACCINATED, WAS_DESTROYED = values[1], values[2], values[3], values[4] 
                command = 'UPDATE Results_unitstats ' \
                          ' SET cumulative_infected=cumulative_infected+%i,' \
                          ' cumulative_zone_focus=cumulative_zone_focus+%i,' \
                          ' cumulative_vaccinated=cumulative_vaccinated+%i,' \
                          ' cumulative_destroyed=cumulative_destroyed+%i' \
                          ' WHERE unit_id=%s' % (1 if WAS_INFECTED else 0, 1 if WAS_ZONE_FOCUS else 0, 1 if WAS_VACCINATED else 0, 1 if WAS_DESTROYED else 0, unit)

                cursor = connections['scenario_db'].cursor()
                cursor.execute(command)

                # Results.models.UnitStats.objects.filter(unit__id=values[0]).update(
                #     cumulative_infected=F("cumulative_infected") + 1 if values[1] else 0,
                #     cumulative_destroyed=F("cumulative_destroyed") + 1 if values[4] else 0,
                #     cumulative_vaccinated=F("cumulative_vaccinated") + 1 if values[3] else 0,
                #     cumulative_zone_focus=F("cumulative_zone_focus") + 1 if values[2] else 0)
                return True
            except BaseException as e:
                print("Command Failure", e, command)
                pass
        return False
