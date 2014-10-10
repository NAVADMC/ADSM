from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from collections import OrderedDict
from future import standard_library
standard_library.install_hooks()

from Results.models import DailyControls, DailyByProductionType, DailyByZone
from ScenarioCreator.models import Zone, OutputSettings
from django.db.models import Q


def list_of_iterations():
    return list(DailyControls.objects.values_list('iteration', flat=True).distinct())


def median_value(queryset, term):
    count = queryset.count()
    try:
        return queryset.values_list(term, flat=True).order_by(term)[int(round(count/2))]
    except:
        return 0


def last_day_query(model=DailyControls):
    last_days = {}  # dictionary with iteration int keys
    for iteration in list_of_iterations():
        last_days[iteration] = model.objects.filter(iteration=iteration).order_by('day').last().day
    last_day_query1 = [Q(iteration=key, day=value) for key, value in last_days.items()]
    return reduce(Q.__or__, last_day_query1, Q(day=-1))


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


def pair(unit_pair, animal_number):
    return unit_pair[0], "%i (%i)" % (unit_pair[1], animal_number)


def summarize_results():
    summary = OrderedDict()
    summary["Unit (Animal) Summary"] = [
        pair(name_and_value("infcU"), field_summary("infcA")),
        pair(name_and_value("firstDetUInf", DailyControls), field_summary("firstDetAInf", DailyControls)),
        pair(name_and_value("descU"), field_summary("descA")),
        pair(name_and_value("vaccU"), field_summary("vaccA"))]
    summary["Days Summary"] = [
        name_and_value("outbreakDuration", DailyControls),
        name_and_value("diseaseDuration", DailyControls),
        name_and_value("firstDetection"),
        name_and_value("firstVaccination"),
        name_and_value("firstDestruction"),
        name_and_value("maxZoneArea", DailyByZone)]

    return summary

def iteration_progress():
    output_settings = OutputSettings.objects.get_or_create()[0]
    iterations_started = output_settings.iterations
    stop_criteria = output_settings.stop_criteria

    calculation_function = {
        "disease-end": lambda: DailyControls.objects.filter(last_day_query(), diseaseDuration__gt=0).count(),
        "first-detection": lambda: DailyByProductionType.objects
                                    .filter(last_day_query(model=DailyByProductionType), firstDetection__gt=0)
                                    .values_list('iteration', flat=True).distinct().count(),
        "outbreak-end": lambda: DailyControls.objects.filter(last_day_query(), outbreakDuration__gt=0).count(),
        "stop-days": lambda: DailyControls.objects.filter(last_day_query(), day=OutputSettings.objects.get().days).count(),
    }

    first_iteration_half_done = 0.5
    try:
        iterations_completed = calculation_function[stop_criteria]() or first_iteration_half_done
    except KeyError:
        raise NotImplementedError("'%s' does not have an implemented progress calculation function." % stop_criteria)
    return iterations_completed / iterations_started if iterations_started else 0
