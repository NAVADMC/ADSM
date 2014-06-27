from ast import literal_eval
import Results.models


def save_value_to_proper_field(c_header_name, value, iteration, day):
    daily_tables = [Results.models.DailyControls(), ]
        # Results.models.DailyByZoneAndProductionType(), Results.models.DailyByZone(), Results.models.DailyByProductionType()]
    # DailyByProductionType is listed last because it has the most compositing.
    for table in daily_tables:
        for name, obj in table:
            if str(name) == str(c_header_name):
                print("==Storing==", name, obj, value)
                table_instance = type(table).objects.get_or_create(iteration=iteration, day=day)[0]
                setattr(table_instance, name, value)
                table_instance.save()
                return True
    # getattr(type(self.instance), field).field.rel.to
    # parentObj._meta.get_field('myField').rel.to
    return False


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