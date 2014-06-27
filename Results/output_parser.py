from ast import literal_eval
import re
import Results.models
from ScenarioCreator.models import Zone, ProductionType


def match_DailyControls(c_header_name, day, iteration, value):
    table = Results.models.DailyControls()
    for name, obj in table:
        if str(name) == str(c_header_name):
            table_instance = type(table).objects.get_or_create(iteration=iteration, day=day)[0]
            setattr(table_instance, name, value)
            table_instance.save()
            return True
    return False


def camel_case_spaces(zone_description):
    return re.sub(r' (\w)', lambda match: match.group(1).upper(), zone_description)


def extract_name(c_header_name, possibilities):
    """Returns the header with the name clipped out and the matching name if it is in the list of possibilities.
     Use for extracting zone and production type names from CEngine output."""
    for name in possibilities:
        if camel_case_spaces(name) in c_header_name:  # It's important to camelCase this to match C output
            shortened = re.sub(camel_case_spaces(name), '', c_header_name)
            return shortened, name
    return c_header_name, None


def match_DailyByZone(c_header_name, day, iteration, value):
    possibilities = {x.zone_description for x in Zone.objects.all()}.union({'Background'})
    c_header_name, zone = extract_name(c_header_name, possibilities)
    if not zone:
        return False
    target_zone = None
    if zone != 'Background':
        target_zone = Zone.objects.get(zone_description=zone)  # we don't want to get_or_create because I want to keep "Background" out of the DB.

    table = Results.models.DailyByZone()
    for name, obj in table:
        if str(name) == str(c_header_name):
            table_instance = type(table).objects.get_or_create(iteration=iteration, day=day, zone=target_zone)[0]
            setattr(table_instance, name, value)
            table_instance.save()
            return True
    return False


def match_DailyByZoneAndProductionType(c_header_name, day, iteration, value):
    possible_zones = {x.zone_description for x in Zone.objects.all()}.union({'Background'})
    possible_pts = {x.name for x in ProductionType.objects.all()}
    c_header_name, zone = extract_name(c_header_name, possible_zones)
    c_header_name, pt = extract_name(c_header_name, possible_pts)
    if not zone or not pt:  # it only belongs on this table if it matches both
        return False
    target_zone = None

    if zone != 'Background':
        target_zone = Zone.objects.get(zone_description=zone)  # we don't want to get_or_create because I want to keep "Background" out of the DB.
    pt = ProductionType.objects.get(name=pt)  # TODO: handle the '' blank case in Production Type

    table = Results.models.DailyByZoneAndProductionType()
    for name, obj in table:
        if str(name) == str(c_header_name):
            print('==Storing==', name)
            table_instance = type(table).objects.get_or_create(iteration=iteration, day=day, zone=target_zone, production_type=pt)[0]
            setattr(table_instance, name, value)
            table_instance.save()
            return True
    return False


def save_value_to_proper_field(c_header_name, value, iteration, day):
    c_header_name = re.sub('-', '_', c_header_name)  #TODO: a couple of names use hyphens.  Preferrably have them renamed on the C side
        # Results.models.DailyByZoneAndProductionType(), Results.models.DailyByZone(), Results.models.DailyByProductionType()]
    # DailyByProductionType is listed last because it has the most compositing.

    if match_DailyControls(c_header_name, day, iteration, value) or \
            match_DailyByZone(c_header_name, day, iteration, value) or \
            match_DailyByZoneAndProductionType(c_header_name, day, iteration, value):
        print("Match found for:", c_header_name)
    # else:
    #     print("-No match for:", c_header_name)
    # getattr(type(self.instance), field).field.rel.to
    # parentObj._meta.get_field('myField').rel.to


def populate_db_from_daily_report(sparse_info):
    """Parses the C Engine stdout and populates the appropriate models with the information.  Takes one line
    at a time, representing one DailyReport."""
    assert isinstance(sparse_info, dict)
    # sparse_info = literal_eval(report.sparse_dict)
    print(sparse_info)
    iteration = sparse_info['Run']
    del sparse_info['Run']
    day = sparse_info['Day']
    del sparse_info['Day']
    for c_header_name, value in sparse_info.items():
        save_value_to_proper_field(c_header_name, value, iteration, day)