from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from collections import defaultdict
from future.builtins import *
from future import standard_library
standard_library.install_hooks()

from concurrent.futures import ProcessPoolExecutor
from glob import glob
import platform
import threading
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect
from django.conf import settings
import subprocess
import time
from ScenarioCreator.models import OutputSettings
from django.db.models import Max
from Results.models import *  # necessary
from Results.forms import *  # necessary
import Results.output_parser
from Results.summary import list_of_iterations, summarize_results


def back_to_inputs(request):
    return redirect('/setup/')


def prepare_supplemental_output_directory():
    """Creates a directory with the same name as the Scenario and directs the Simulation to store supplemental files in the new directory"""
    output_args = []
    if any(OutputSettings.objects.values('save_daily_unit_states', 'save_daily_events', 'save_daily_exposures', 'save_iteration_outputs_for_units',
                                         'save_map_output')[0].values()):  # any of these settings would justify an output directory
        output_dir = os.path.join('workspace', scenario_filename())  # this does not have the .sqlite3 suffix
        output_args = ['--output-dir', output_dir]  # to be returned and passed to adsm.exe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    return output_args


def non_empty_lines(line):
    output_lines = []
    line = line.decode("utf-8").strip()
    if len(line):
        output_lines += line.split('\n')  # entries can be more than one line
    return output_lines


def simulation_process(iteration_number):
    start = time.time()
    output_args = prepare_supplemental_output_directory()
    executables = {"Windows": 'adsm.exe', "Linux": 'adsm'}
    system_executable = os.path.join(settings.BASE_DIR, executables[platform.system()])  #TODO: KeyError
    simulation = subprocess.Popen([system_executable, '-i', str(iteration_number), 'activeSession.sqlite3'] + output_args,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    headers = simulation.stdout.readline().decode("utf-8")  # first line should be the column headers
    # print(headers)
    parser = Results.output_parser.DailyParser(headers)

    for line in iter(simulation.stdout.readline, b''):  #
        parser.parse_daily_strings(non_empty_lines(line))
    outs, errors = simulation.communicate()  # close p.stdout, wait for the subprocess to exit
    if errors:  # this will only print out error messages after the simulation has halted
        print(errors)
    # TODO: When the subprocess terminates there might be unconsumed output that still needs to be processed.
    # (I haven't seen evidence of uncaught output since 10 days after writing it)
    end = time.time()
    return '%i: Success in %i seconds' % (iteration_number, end-start)


class Simulation(threading.Thread):
    """Execute system commands in a separate thread so as not to interrupt the webpage.
    Saturate the computer's processors with parallel simulation iterations"""
    def __init__(self, max_iteration, **kwargs):
        self.max_iteration = max_iteration
        super(Simulation, self).__init__(**kwargs)

    def run(self):
        # print(simulation_process())
        statuses = []
        with ProcessPoolExecutor() as executor:
            for exit_status in executor.map(simulation_process, range(1, self.max_iteration+1)):
                statuses.append(exit_status)
        print(statuses)


def results_home(request):
    path_ex = os.path.join("workspace", scenario_filename(), "*.txt")
    context = {'supplemental_files': [re.sub(r'workspace/?', '', re.sub(r'\\', '/', path)) for path in glob(path_ex)]}
    # TODO: value dict file sizes
    if DailyControls.objects.all().count() > 0:
        context['summary'] = Results.summary.summarize_results()
        context['iterations'] = len(list_of_iterations())
    return render(request, 'Results/SimulationProgress.html', context)


def run_simulation(request):
    delete_all_outputs()
    sim = Simulation(OutputSettings.objects.all().first().iterations)
    sim.start()  # starts a new thread
    return redirect('/results/')


def list_entries(model_name, model, iteration=1):
    return model.objects.filter(iteration=iteration)[:200],


def graph_field_by_zone(request, model_name, field_name, iteration=None):
    links = [request.path + zone + '/Graph.png' for zone in Zone.objects.all().values_list('name', flat=True)]
    iter_str = "iteration " + str(iteration) if iteration else 'for all iterations'
    context = {'title': "Graph of %s in %s %s" % (field_name, model_name, iter_str),
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


def empty_fields(model_class, excluded_fields):
    rejected_fields = []
    target_fields = [field for field in model_class._meta.get_all_field_names() if field not in excluded_fields]
    maximums_dict = model_class.objects.all().aggregate(*[Max(field) for field in target_fields])
    for key, value in maximums_dict.items():
        if value is None or value <= 0:
            rejected_fields.append(key[:-5])  # 5 characters in '__max'
    return rejected_fields


def class_specific_headers(model_name, prefix):
    # this mapping is also embedded in navigationPanel.html
    headers = {'DailyByProductionType': [("Exposures", "exp", 'expcU'),
                                         ("Infections", "inf", 'infcU'),
                                         ("Destruction", "des", 'descU'),
                                         ("Exams", "exm", 'exmcUAll'),
                                         ("Lab Tests", "tst", 'tstcUAll'),
                                         ("Tracing", "tr", 'trcUAll')],
               'DailyControls': [("Destruction", 'dest', 'destrSubtotal'),
                                 ("Destruction Wait", 'desw', 'deswATimeAvg'),
                                 ("Vaccination", 'vac', 'vaccVaccination')]}
    headers = defaultdict(lambda: [('', '', '')], headers)
    headers = headers[model_name]  # select by class
    if prefix:  # filter if there's a prefix
        headers = [item for item in headers if item[1] == prefix]
        title, pref, link = headers[0]
        headers[0] = title, pref, '/results/' + model_name + '/' + headers[0][2]  # otherwise links get broken
    return headers


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
        context['excluded_fields'] = ['zone', 'production_type', 'day', 'iteration', 'id', 'pk']
        context['excluded_fields'] += [field for field in model_class._meta.get_all_field_names() if not field.startswith(prefix)]
        context['empty_fields'] = empty_fields(model_class, context['excluded_fields'])
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



