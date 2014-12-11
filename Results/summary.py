from collections import OrderedDict
from Results.models import DailyControls, DailyByProductionType, DailyByZone
from ScenarioCreator.models import Zone
from ScenarioCreator.models import Zone, OutputSettings
from django.db.models import Q


def list_of_iterations():
    return list(DailyControls.objects.values_list('iteration', flat=True).distinct())


def median_value(queryset, term):
    count = queryset.count()
    try:
        med = queryset.values_list(term, flat=True).order_by(term)[int(round(count / 2))]
        return med if med != -1 else "N/A"
    except:
        return "N/A"


def last_day_query(model=DailyControls):
    return Q(last_day=True)


def field_summary(field_name, model=DailyByProductionType):
    # switch on model
    if model == DailyByProductionType:  # query only the "All" production type on the last day of each iteration
        queryset = DailyByProductionType.objects.filter(last_day_query(), production_type=None)
    elif model == DailyControls:
        queryset = DailyControls.objects.filter(last_day_query())
    else:  # zone
        zone = Zone.objects.all().order_by('radius').last()
        queryset = DailyByZone.objects.filter(last_day_query(), zone=zone)

    return median_value(queryset, field_name)  # value list, last day, median, aggregate


def name(field_name, model=DailyByProductionType):
    return model._meta.get_field_by_name(field_name)[0].verbose_name


def name_and_value(field_name, model=DailyByProductionType):
    return name(field_name, model), field_summary(field_name, model)


def pair(unit_number, animal_number):
    return "%s (%s)" % (str(unit_number), str(animal_number))


def summarize_results():
    summary = OrderedDict()
    summary["Unit (Animal) Summary"] = [
        ("Median Infected Units (Animals)", pair(field_summary("infcU"), field_summary("infcA"))),
        ("Median Units (Animals) Infected at First Detection", pair(field_summary("firstDetUInf", DailyControls), field_summary("firstDetAInf", DailyControls))),
        ("Median Depopulated Units (Animals)", pair(field_summary("descU"), field_summary("descA"))),
        ("Median Vaccinated Units (Animals)", pair(field_summary("vaccU"), field_summary("vaccA")))]
    summary["Event Summary"] = [
        ("Median Outbreak Duration in Days (end of control activities)", 
            field_summary("outbreakDuration", DailyControls)),
        ("Median Duration of Disease Spread in Days",field_summary("diseaseDuration", DailyControls)),
        ("Median Day of First Detection", field_summary("firstDetection")),
        ("Median Day of First Vaccination", field_summary("firstVaccination")),
        ("Median Day of First Destruction", field_summary("firstDestruction"))]
    zones_summary = []
    for zone in Zone.objects.all():
        queryset = DailyByZone.objects.filter(last_day_query(), zone=zone)
        zones_summary.append(
            ("Median Total Area of %s in km^2" % zone.name, median_value(queryset, "zoneArea")))
        zones_summary.append(
            ("Median Number of Distinct %s Zones" % zone.name, median_value(queryset, "numSeparateAreas")))
    summary["Zone Summary"] = zones_summary
    
    return summary


def iteration_progress():
    output_settings = OutputSettings.objects.get_or_create()[0]
    iterations_started = output_settings.iterations
    stop_criteria = output_settings.stop_criteria

    calculation_function = {
        "disease-end": lambda: DailyControls.objects.filter(last_day_query(), diseaseDuration__gt=0).count(),
        "first-detection": lambda: DailyByProductionType.objects
                                    .filter(last_day_query(model=DailyByProductionType), firstDetection__gt=0, production_type=None)
                                    .values_list('iteration', flat=True).distinct().count(),
        # these last two have an implicit last_day_query because outbreakDuration is the last event in a simulation
        "outbreak-end": lambda: DailyControls.objects.filter(outbreakDuration__gt=0).count(),
        "stop-days": lambda: DailyControls.objects.filter(Q(day=OutputSettings.objects.get().days) | Q(outbreakDuration__gt=0)).count(),
    }

    first_iteration_half_done = 0.5
    try:
        iterations_completed = calculation_function[stop_criteria]() or first_iteration_half_done
    except KeyError:
        raise NotImplementedError("'%s' does not have an implemented progress calculation function." % stop_criteria)
    return iterations_completed / iterations_started if iterations_started else 0


def iterations_complete():
    output_settings = OutputSettings.objects.get_or_create()[0]
    stop_criteria = output_settings.stop_criteria

    calculation_function = {
        "disease-end": lambda: DailyControls.objects.filter(last_day_query(), diseaseDuration__gt=0).count(),
        "first-detection": lambda: DailyByProductionType.objects
                                    .filter(last_day_query(model=DailyByProductionType), firstDetection__gt=0, production_type=None)
                                    .values_list('iteration', flat=True).distinct().count(),
        # these last two have an implicit last_day_query because outbreakDuration is the last event in a simulation
        "outbreak-end": lambda: DailyControls.objects.filter(outbreakDuration__gt=0).count(),
        "stop-days": lambda: DailyControls.objects.filter(Q(day=OutputSettings.objects.get().days) | Q(outbreakDuration__gt=0)).count(),
    }

    try:
        iterations_completed = calculation_function[stop_criteria]()
    except KeyError:
        raise NotImplementedError("'%s' does not have an implemented progress calculation function." % stop_criteria)
    return iterations_completed
