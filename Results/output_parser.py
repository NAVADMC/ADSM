from ast import literal_eval
from collections import namedtuple
import re
from django.db.models import ForeignKey
import Results.models
from ScenarioCreator.models import Zone, ProductionType

GrammarPath = namedtuple('GrammarPath', ['prefix', 'group_class', 'suffix'])


possible_zones = {x.zone_description for x in Zone.objects.all()}.union({'Background'})
possible_pts = {x.name for x in ProductionType.objects.all()}


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


def match_DailyControls(c_header_name, day, iteration, value):
    table = Results.models.DailyControls()
    if not any([c_header_name.startswith(x[0]) for x in table]):  # it only belongs on this table if it matches a field name
        return False

    for name, obj in table:
        if str(name) == str(c_header_name):
            table_instance = type(table).objects.get_or_create(iteration=iteration, day=day)[0]
            setattr(table_instance, name, value)
            table_instance.save()
            return True
    return False


def match_DailyByZone(c_header_name, day, iteration, value):
    table = Results.models.DailyByZone()
    if not any([c_header_name.startswith(x[0]) for x in table]):  # it only belongs on this table if it matches a field name
        return False

    possibilities = {x.zone_description for x in Zone.objects.all()}.union({'Background'})
    c_header_name, zone = extract_name(c_header_name, possibilities)
    if not zone:
        return False
    target_zone = None
    if zone != 'Background':
        target_zone = Zone.objects.get(zone_description=zone)  # we don't want to get_or_create because I want to keep "Background" out of the DB.

    for name, obj in table:
        if str(name) == str(c_header_name):
            table_instance = type(table).objects.get_or_create(iteration=iteration, day=day, zone=target_zone)[0]
            setattr(table_instance, name, value)
            table_instance.save()
            return True
    return False


def match_DailyByZoneAndProductionType(c_header_name, day, iteration, value):
    table = Results.models.DailyByZoneAndProductionType()
    if not any([c_header_name.startswith(x[0]) for x in table]):  # it only belongs on this table if it matches a field name
        return False

    possible_zones = {x.zone_description for x in Zone.objects.all()}.union({'Background'})
    possible_pts = {x.name for x in ProductionType.objects.all()}
    c_header_name, zone = extract_name(c_header_name, possible_zones)
    c_header_name, pt = extract_name(c_header_name, possible_pts)

    target_zone = None
    if zone != 'Background':
        target_zone = Zone.objects.get(zone_description=zone)  # we don't want to get_or_create because I want to keep "Background" out of the DB.
    try:  # handles the '' blank case in Production Type
        pt = ProductionType.objects.get(name=pt)
    except: pass

    for name, obj in table:
        if str(name) == str(c_header_name):
            table_instance = type(table).objects.get_or_create(iteration=iteration, day=day, zone=target_zone, production_type=pt)[0]
            setattr(table_instance, name, value)
            table_instance.save()
            return True
    return False


def match_DailyByProductionType(c_header_name, day, iteration, value, composite_field_map):
    possible_pts = {x.name for x in ProductionType.objects.all()}
    c_header_name, pt = extract_name(c_header_name, possible_pts)
    matching_composites = [x for x in composite_field_map.keys() if c_header_name == x]
    if not matching_composites:  # it only belongs on this table if it matches a field name
        return False
    if len(matching_composites) > 1:  # this happens with the p suffix
        print('  **Multiple matches:', matching_composites)


    try:  # handles the '' blank case in Production Type
        pt = ProductionType.objects.get(name=pt)
    except:
        pass

    table = Results.models.DailyByProductionType()
    field_name = matching_composites[0]
    path = composite_field_map[field_name]
    table_instance = type(table).objects.get_or_create(iteration=iteration, day=day, production_type=pt)[0]
    if isinstance(path, str):
        setattr(table_instance, field_name, value)
        table_instance.save()
        return True
    elif isinstance(path, GrammarPath):
        stat_group = getattr(table_instance, path.prefix)
        if not stat_group:  # we need to create the first statGroup attached to the Foreign key
            saved_instance = path.group_class()
            saved_instance.save()
            setattr(table_instance, path.prefix, saved_instance)
            stat_group = getattr(table_instance, path.prefix)
        setattr(stat_group, path.suffix, value)
        stat_group.save()
        table_instance.save()
        return True

    return False


def save_value_to_proper_field(c_header_name, value, iteration, day, composite_field_map):
    c_header_name = re.sub('-', '_', c_header_name)  #TODO: a couple of names use hyphens.  Preferrably have them renamed on the C side

    return match_DailyControls(c_header_name, day, iteration, value) or \
            match_DailyByZone(c_header_name, day, iteration, value) or \
            match_DailyByZoneAndProductionType(c_header_name, day, iteration, value) or \
            match_DailyByProductionType(c_header_name, day, iteration, value, composite_field_map)  # DailyByProductionType is listed last because it has the most compositing.


def not_blank(suffix):
    if suffix != '_blank':
        return suffix
    return ''


def build_composite_field_map(table):
    road_map = {}
    for prefix, field in table:
        if prefix not in ('iteration', 'day', 'production_type', 'zone'):  # skip the selector fields
            road_map[prefix] = prefix
            pref_all = prefix.replace('All', '')
            if pref_all not in road_map:
                road_map[pref_all] = prefix  # special case where C removes All when suffixed by a Production Type

    return road_map


def stripped_field(c_header_name):
    c_header_name, zone = extract_name(c_header_name, possible_zones)
    c_header_name, pt = extract_name(c_header_name, possible_pts)
    return c_header_name


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

    #refresh the values already declared at the top of this file.
    globals()['possible_zones'] = {x.zone_description for x in Zone.objects.all()}.union({'Background'})
    globals()['possible_pts'] = {x.name for x in ProductionType.objects.all()}

    tables = [Results.models.DailyByProductionType(), Results.models.DailyByZone(),
              Results.models.DailyByZoneAndProductionType(), Results.models.DailyControls()]
    field_map = {table: build_composite_field_map(table) for table in tables}

    #construct the set of tables we're going to use for this day
    daily_by_pt = {pt.name: Results.models.DailyByProductionType(production_type=pt, iteration=iteration, day=day) for pt in ProductionType.objects.all()}
    daily_by_zone = {zone.zone_description: Results.models.DailyByZone(zone=zone, iteration=iteration, day=day) for zone in Zone.objects.all()}
    daily_by_pt_zone = {}  # same as above, the double loop was a bit much for a dict comprehension
    for pt in ProductionType.objects.all():
        for zone in Zone.objects.all():
            #stored by immutable tuple
            daily_by_pt_zone[(pt.name, zone.zone_description)] = \
                Results.models.DailyByZoneAndProductionType(production_type=pt, zone=zone, iteration=iteration, day=day)

    failures = []
    for pt in daily_by_pt:
        matching_fields = [field for field in sparse_info if pt in field]  # fields with this production type in them
        for field in matching_fields:  # Populate DailyByProductionType
            setattr(daily_by_pt[pt], stripped_field(field),  sparse_info[field])
        #for each zone
            #create and populate DailyByZoneAndProductionType
        daily_by_pt[pt].save()
    #for each zone
        #populate DailyByZone
    #populate DailyControls

    #whatever is left is a failure

    # for c_header_name, value in sparse_info.items():
    #     if save_value_to_proper_field(c_header_name, value, iteration, day, composite_field_map):
    #         successes.append(c_header_name)
    #     elif 'c' not in [c_header_name[2], c_header_name[3]]:
    #         failures.append(c_header_name)
    print('failures', len(failures))
    print(failures)
