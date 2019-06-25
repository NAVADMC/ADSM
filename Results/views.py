from collections import defaultdict
from itertools import chain
import os
from glob import glob

from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect
from django.db.models import Max
from django.utils.html import mark_safe

from ADSMSettings.models import SmSession
from ADSMSettings.utils import workspace_path, scenario_filename
from ScenarioCreator.models import OutputSettings
from Results.graphing import construct_title
from Results.forms import *  # necessary
from Results.simulation import Simulation
from Results.utils import delete_supplemental_folder, map_zip_file, delete_all_outputs, is_simulation_stopped, is_simulation_running
import Results.output_parser
from Results.summary import list_of_iterations, iterations_complete
from Results.csv_generator import SummaryCSVGenerator, SUMMARY_FILE_NAME
from Results.combine_outputs import CombineOutputsGenerator


def back_to_inputs(request):
    return redirect('/setup/OutputSettings/1')


def simulation_status(request):
    output_settings = OutputSettings.objects.get()
    status = {
        'is_simulation_stopped': is_simulation_stopped(),
        'simulation_has_started': SmSession.objects.get().simulation_has_started,
        'iterations_total': output_settings.iterations,
        'iterations_started': len(list_of_iterations()),
        'iterations_completed': iterations_complete(),
        'iteration_text': mark_safe(SmSession.objects.get().iteration_text),
    }
    return JsonResponse(status)


def results_home(request):
    from Results.csv_generator import SUMMARY_FILE_NAME
    path_ex = workspace_path(scenario_filename() + "/" + "Supplemental Output Files")
    start = workspace_path()
    context = {'supplemental_files': [os.path.relpath(file_path, start=start) for file_path in glob(path_ex + "/*.csv")]}

    for combined_file in [os.path.relpath(file_path, start=start) for file_path in glob(path_ex + "/Combined Outputs/*.txt")]:
        context['supplemental_files'].append(combined_file)
    for combined_file in [os.path.relpath(file_path, start=start) for file_path in glob(path_ex + "/Combined Outputs/*.csv")]:
        context['supplemental_files'].append(combined_file)

    summary_path = os.path.join(scenario_filename(), SUMMARY_FILE_NAME)
    try:
        context['supplemental_files'].remove(summary_path)
    #             context['supplemental_files'] = [file for file in context['supplemental_files'] if not file.endswith(SUMMARY_FILE_NAME)] # filter out summary.csv
    except ValueError:
        pass
    context['summary_file_name'] = summary_path

    if os.path.exists(map_zip_file()):
        context['supplemental_files'].append(os.path.relpath(map_zip_file(), start=start))
    # TODO: value dict file sizes
    if DailyControls.objects.all().count() > 0:
        context['summary'] = Results.summary.summarize_results()
        context['iterations'] = len(list_of_iterations())
        context['population_eta'] = Unit.objects.count() / 650  # estimate slow map calc in matplotlib
        try:
            v = ResultsVersion.objects.get()
            context['version_number'] = '.'.join([v.versionMajor, v.versionMinor, v.versionRelease])
        except:  # more specific exceptions kept leaking through
            pass

    # get the had_memory_error boolean, this is used to display the error banner.
    sm_session = SmSession.objects.get()
    context['had_memory_error'] = sm_session.had_memory_error

    return render(request, 'Results/SimulationProgress.html', context)


def create_blank_unit_stats():
    """This is intended to run before the simulation has a chance to complete and begin writing output.
    I've set this up before the ProcessPoolExecutor call to avoid a race condition."""
    python_objs = []
    print("Starting Unit Stat creation")
    for unit in Unit.objects.all():  # or .filter(unitstats__isnull=True)
        python_objs.append(UnitStats(unit=unit))
    UnitStats.objects.bulk_create(python_objs)
    print("Finished Unit Stat creation")


def run_simulation(request):
    delete_all_outputs()
    delete_supplemental_folder()
    create_blank_unit_stats()  # create UnitStats before we risk the simulation writing to them
    sim = Simulation(OutputSettings.objects.all().first().iterations)
    sim.start()  # starts a new thread
    # time.sleep(5) # give initial threads time to initialize their db connection
    return redirect('/results/')


def list_entries(model_name, model, iteration=1):
    return model.objects.filter(iteration=iteration)[:200],


def graph_field_by_zone(request, model_name, field_name, iteration=None):
    links = [request.path + zone + '/Graph.png' for zone in Zone.objects.all().values_list('name', flat=True)]
    explanation, title = construct_title(field_name, iteration, globals()[model_name])
    context = {'title': title,
               'image_links': links}
    return render(request, 'Results/Graph.html', context)


def graph_field(request, model_name, field_name, iteration=None):
    if model_name in ['DailyByZoneAndProductionType', 'DailyByZone']:
        return graph_field_by_zone(request, model_name, field_name, iteration)
    if not iteration:
        print("Blank Iteration:", request.path)
    iter_str = "iteration " + str(iteration) if iteration else 'for all iterations'
    context = {'title': "Graph of %s in %s %s" % (field_name, model_name, iter_str),
               'image_links': [request.path + 'Graph.png']}
    return render(request, 'Results/Graph.html', context)


def empty_fields(target_fields_by_model_class):
    """Expects a dictionary:  key=model_class, value=target_fields list"""
    rejected_fields = []
    for model_class in target_fields_by_model_class.keys():
        target_fields = target_fields_by_model_class[model_class]
        maximums_dict = model_class.objects.all().aggregate(*[Max(field) for field in target_fields])
        for key, value in maximums_dict.items():
            if value is None or value <= 0:
                rejected_fields.append(key[:-5])  # 5 characters in '__max'
    return rejected_fields


def all_empty_fields(model_class, excluded_fields):
    """Returns a list of all empty fields for a single model"""
    target_fields = [field for field in model_class._meta.get_all_field_names() if field not in excluded_fields]
    return empty_fields({model_class: target_fields})


# this mapping is also embedded in navigationPanel.html
headers = {'DailyByProductionType': [("Exposures", "exp", ['expnU', 'expcU']),
                                     ("Infections", "inf", ['infnU', 'infcU']),
                                     ("Detections", "det", ['detnU', 'detcU']),
                                     ("Vaccinations", "vac", ['vacnU', 'vaccU']),
                                     ("Destruction", "des", ['desnU', 'descU']),
                                     ("Exams", "exm", ['exmnU', 'exmcU']),
                                     ("Lab Tests", "tst", ['tstnU', 'tstcU']),
                                     ("Tracing", "tr", ['trnU', 'trcU'])],
           #'DailyControls': [("Destruction", 'dest', ['destrSubtotal']),  # TODO: figure out why DailyControls subcategories are not displaying right
           #                  ("Destruction Wait", 'desw', ['deswUTimeAvg']),
           #                  ("Vaccination", 'vacc', ['vaccVaccination'])]
           }
headers = defaultdict(lambda: [('', '', [])], headers)


def class_specific_headers(model_name, prefix):
    sub_headers = headers[model_name]  # select by class
    hidden_categories = excluded_headers()
    if prefix:  # filter if there's a prefix
        sub_headers = [item for item in sub_headers if item[1] == prefix]
        title, pref, links = sub_headers[0]
        links = ['/results/' + model_name + '/' + item for item in links]  # otherwise links get broken
        sub_headers[0] = title, pref, links
    else:
        sub_headers = [item for item in sub_headers if item[1] not in hidden_categories.keys()]
    return sub_headers


def model_class(model_name):
    return globals()[model_name]  # IMPORTANT: depends on import *


def excluded_headers():
    """Returns a dictionary containing the names of excluded results subcategories for the context processor.
    The values are CSS classes inserted in the template navigationPane.html"""
    subcategory_states = {}
    bad_fields = empty_fields({model_class(key): list(chain(*[v[2] for v in value])) for key, value in headers.items()})
    for bad_field in bad_fields:
        for sub_list in headers.values():
            for entry in sub_list:
                if bad_field in entry[2]:
                    subcategory_states[entry[1]] = 'empty_subcategory'  # This is a CSS class
    return subcategory_states


def result_table(request, model_name, model_class, model_form, graph_links=False, prefix=''):
    """Displays a table with links to all possible graphs of each field, for every iteration.
       Issue #127"""
    ResultSet = modelformset_factory(model_class, extra=0, form=model_form)
    iterations = list_of_iterations()
    context = {'title': 'Results from %i Iterations' % len(iterations)}
    if not graph_links:  # Old behavior with a number table, only first 50 entries, useful for debug
        context['formset'] = ResultSet(queryset=model_class.objects.all().order_by('iteration', 'day')[:50])
        return render(request, 'Results/FormSet.html', context)
    else:  # New Behavior with links to a graph for every field
        context['formset'] = ResultSet(queryset=model_class.objects.all().order_by('iteration', 'day')[:5])
        context['Zones'] = Zone.objects.all()
        context['iterations'] = iterations[:5]  # It's pointless to display links to more than the first 10 iterations, there can be thousands
        context['model_name'] = model_name
        context['excluded_fields'] = ['zone', 'production_type', 'day', 'iteration', 'id', 'pk', 'last_day']
        context['excluded_fields'] += [field for field in model_class._meta.get_all_field_names() if not field.startswith(prefix)]
        context['empty_fields'] = all_empty_fields(model_class, context['excluded_fields'])
        context['headers'] = class_specific_headers(model_name, prefix)
        return render(request, 'Results/GraphLinks.html', context)


def get_model_name_and_model(request):
    """A slight variation on get_mode_name_and_form useful for cases where you don't want a form"""
    model_name = re.split('\W+', request.path)[2]  # Second word in the URL
    model = globals()[model_name]  # IMPORTANT: depends on import *
    return model_name, model


def model_list(request):
    model_name, model = get_model_name_and_model(request)
    return result_table(request, model_name, model, globals()[model_name+'Form'], True)
    # context = {'title': spaces_for_camel_case(model_name),
    #            'class': model_name,
    #            'name': spaces_for_camel_case(model_name),
    #            'entries': list_entries(model_name, model)}
    # return render(request, 'Results/ResultTable.html', context)


def filtered_list(request, prefix):
    model_name, model = get_model_name_and_model(request)
    return result_table(request, model_name, model, globals()[model_name + 'Form'], True, prefix)


def summary_csv(request):
    class HttpResponseAccepted(HttpResponse):
        status_code = 202

    if request.method == "GET":
        if SmSession.objects.get().calculating_summary_csv:
            return HttpResponseAccepted()
        elif not DailyControls.objects.all().count() or is_simulation_running():
            return HttpResponseBadRequest()
        elif not os.path.isfile(workspace_path(scenario_filename() + "/" + "Supplemental Output Files" + '/' + SUMMARY_FILE_NAME)):
            return HttpResponseNotFound()
        else:
            return HttpResponse()
    if request.method == "POST":
        csv_generator = SummaryCSVGenerator()
        csv_generator.start()  # starts a new thread
        return HttpResponseAccepted()
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def combine_outputs(request):

    class HttpResponseAccepted(HttpResponse):
        status_code = 202

    if request.method == "GET":
        if SmSession.objects.get().combining_outputs:
            return HttpResponseAccepted()
        elif not DailyControls.objects.all().count() or is_simulation_running():
            return HttpResponseBadRequest()
        elif len([file_name for file_name in os.listdir(workspace_path(scenario_filename() + "/" + "Supplemental Output Files/Combined Outputs/"))]) != 4:
            return HttpResponseNotFound()
        else:
            return HttpResponse()
    if request.method == "POST":
        outputs_generator = CombineOutputsGenerator()
        outputs_generator.start()  # starts a new thread
        return HttpResponseAccepted()
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
