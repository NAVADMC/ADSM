from ast import literal_eval
import re
import Results.models
from ScenarioCreator.models import Zone


def match_DailyControls(c_header_name, day, iteration, value):
    table = Results.models.DailyControls()
    for name, obj in table:
        if str(name) == str(c_header_name):
            print("==Storing==", name, obj, value)
            table_instance = type(table).objects.get_or_create(iteration=iteration, day=day)[0]
            setattr(table_instance, name, value)
            table_instance.save()
            return True
    return False


def extract_name(c_header_name, possibilities):
    """Returns the header with the name clipped out and the matching name if it is in the list of possibilities.
     Use for extracting zone and production type names from CEngine output."""
    for name in possibilities:
        if name in c_header_name:
            shortened = re.sub(name, '', c_header_name)
            return shortened, name
    return c_header_name, None


def match_DailyByZone(c_header_name, day, iteration, value):
    c_header_name, zone = extract_name(c_header_name, {x.name for x in Zone.objects.all()}.union({'Background'}))
    if not zone:
        return False
    if zone == 'Background':
        zone_key = None
    else:
        zone_key = Zone.objects.get(name=zone)

    table = Results.models.DailyByZone()
    for name, obj in table:
        if str(name) == str(c_header_name):
            print("==Storing==", name, obj, value)
            table_instance = type(table).objects.get_or_create(iteration=iteration, day=day, zone=zone_key)[0]
            setattr(table_instance, name, value)
            table_instance.save()
            return True
    return False


def save_value_to_proper_field(c_header_name, value, iteration, day):
    c_header_name = re.sub('-', '_', c_header_name)  #TODO: a couple of names use hyphens.  Preferrably have them renamed on the C side
        # Results.models.DailyByZoneAndProductionType(), Results.models.DailyByZone(), Results.models.DailyByProductionType()]
    # DailyByProductionType is listed last because it has the most compositing.


    if match_DailyControls(c_header_name, day, iteration, value) or \
            match_DailyByZone(c_header_name, day, iteration, value):
        print("Match found for:", c_header_name)
    else:
        print("-No match for:", c_header_name)
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