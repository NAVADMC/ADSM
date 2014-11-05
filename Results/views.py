from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from collections import defaultdict
import zipfile
from future.builtins import *
from future import standard_library
from ScenarioCreator.context_processor import supplemental_folder_has_contents

standard_library.install_hooks()


from glob import glob
import threading
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect
from django.db import transaction, close_old_connections
import subprocess
import time
import multiprocessing
from ScenarioCreator.models import OutputSettings
from django.db.models import Max
from Results.models import *  # necessary
from Results.forms import *  # necessary
import Results.output_parser
from Results.summary import list_of_iterations, summarize_results
from Settings.models import scenario_filename
import Results.graphing  # necessary to select backend Agg first
from Results.interactive_graphing import population_zoom_png
from Settings.views import adsm_executable_command, workspace_path, save_scenario


def back_to_inputs(request):
    return redirect('/setup/')


def non_empty_lines(line):
    output_lines = []
    line = line.decode("utf-8").strip()
    if len(line):
        output_lines += line.split('\n')  # entries can be more than one line
    return output_lines


def simulation_process(iteration_number, adsm_cmd, queue, production_types, zones):
    start = time.time()

    simulation = subprocess.Popen(adsm_cmd,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  bufsize=1)
    headers = simulation.stdout.readline().decode("utf-8")
    from Results.output_parser import DailyParser
    p = DailyParser(headers, production_types, zones)
    adsm_result = []
    prev_line = ''
    for line in iter(simulation.stdout.readline, b''):
        adsm_result.extend(p.parse_daily_strings(non_empty_lines(prev_line), False))
        prev_line = line
    adsm_result.extend(p.parse_daily_strings(non_empty_lines(prev_line), last_line=True, create_version_entry=iteration_number==1))
    outs, errors = simulation.communicate()  # close p.stdout, wait for the subprocess to exit
    if errors:  # this will only print out error messages after the simulation has halted
        print(errors)
    
    sorted_results = {}
    sorted_results['DailyReport'] = []
    sorted_results['DailyControls'] = []
    sorted_results['DailyByZoneAndProductionType'] = []
    sorted_results['DailyByProductionType'] = []
    sorted_results['DailyByZone'] = []


    for result in adsm_result:
        result_type = type(result).__name__
        if result_type == 'DailyReport':
            sorted_results['DailyReport'].append(result)
        elif result_type == 'DailyControls':
            sorted_results['DailyControls'].append(result)
        elif result_type == 'DailyByZoneAndProductionType':
            sorted_results['DailyByZoneAndProductionType'].append(result)
        elif result_type == 'DailyByProductionType':
            sorted_results['DailyByProductionType'].append(result)
        elif result_type == 'DailyByZone':
            sorted_results['DailyByZone'].append(result)

    queue.put(sorted_results)

    end = time.time()

    return '%i: Success in %i seconds' % (iteration_number, end-start)


def map_zip_file():
    """This is a file named after the scenario in the folder that's also named after the scenario."""
    return workspace_path(scenario_filename() + '/' + scenario_filename() + " Map Output.zip")


def zip_map_directory_if_it_exists():
    dir_to_zip = workspace_path(scenario_filename() + "/Map")
    if os.path.exists(dir_to_zip) and supplemental_folder_has_contents(subfolder='/Map'):
        zipname = map_zip_file()
        dir_to_zip_len = len(dir_to_zip.rstrip(os.sep)) + 1
        with zipfile.ZipFile(zipname, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            for dirname, subdirs, files in os.walk(dir_to_zip):
                for filename in files:
                    path = os.path.join(dirname, filename)
                    entry = path[dir_to_zip_len:]
                    zf.write(path, entry)
    else:
        print("Folder is empty: ", dir_to_zip)

def process_result(queue):
    results = queue.get()

    DailyReport.objects.bulk_create(results['DailyReport'])
    DailyControls.objects.bulk_create(results['DailyControls'])
    DailyByZoneAndProductionType.objects.bulk_create(results['DailyByZoneAndProductionType'])
    DailyByProductionType.objects.bulk_create(results['DailyByProductionType'])
    DailyByZone.objects.bulk_create(results['DailyByZone'])


class Simulation(threading.Thread):
    """Execute system commands in a separate thread so as not to interrupt the webpage.
    Saturate the computer's processors with parallel simulation iterations"""
    def __init__(self, max_iteration, **kwargs):
        self.max_iteration = max_iteration
        self.production_types = ProductionType.objects.values_list('id', 'name')
        self.zones = Zone.objects.values_list('id', 'name')
        super(Simulation, self).__init__(**kwargs)

    def run(self):
        executable_cmd = adsm_executable_command()  # only want to do this once
        statuses = []
        manager = multiprocessing.Manager()
        pool = multiprocessing.Pool()
        queue = manager.Queue()
        for iteration in range(1, self.max_iteration + 1):
            adsm_cmd = executable_cmd + ['-i', str(iteration)]
            res = pool.apply_async(func=simulation_process, args=(iteration, adsm_cmd, queue, self.production_types, self.zones))
            statuses.append(res)
        pool.close()

        [process_result(queue) for iteration in range(self.max_iteration)]

        pool.join()

        statuses = [status.get() for status in statuses]
        print(statuses)
        population_zoom_png()
        zip_map_directory_if_it_exists()
        save_scenario()
        close_old_connections()


def results_home(request):
    path_ex = os.path.join("workspace", scenario_filename(), "*.csv")
    context = {'supplemental_files': [os.path.relpath(file_path, start="workspace") for file_path in glob(path_ex)]}
    if os.path.exists(map_zip_file()):
        context['supplemental_files'].append(os.path.relpath(map_zip_file(), start="workspace"))
    # TODO: value dict file sizes
    if DailyControls.objects.all().count() > 0:
        context['summary'] = Results.summary.summarize_results()
        context['iterations'] = len(list_of_iterations())
        context['large_population'] = Unit.objects.count() > 10000  # determines slower interactive map vs fast matplotlib
        v = ResultsVersion.objects.get()
        context['version_number'] = '.'.join([v.versionMajor, v.versionMinor, v.versionRelease])
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
    time.sleep(5) # give initial threads time to initialize their db connection
    return redirect('/results/')


def list_entries(model_name, model, iteration=1):
    return model.objects.filter(iteration=iteration)[:200],


def graph_field_by_zone(request, model_name, field_name, iteration=None):
    links = [request.path + zone + '/Graph.png' for zone in Zone.objects.all().values_list('name', flat=True)]
    explanation, title = Results.graphing.construct_title(field_name, iteration, globals()[model_name])
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
    headers = {'DailyByProductionType': [("Exposures", "exp", ['expnU', 'expcU']),
                                         ("Infections", "inf", ['infnU', 'infcU']),
                                         ("Vaccinations", "vac", ['vacnU', 'vaccU']),
                                         ("Destruction", "des", ['desnU', 'descU']),
                                         ("Exams", "exm", ['exmnU', 'exmcU']),
                                         ("Lab Tests", "tst", ['tstnU', 'tstcU']),
                                         ("Tracing", "tr", ['trnU', 'trcU'])],
               'DailyControls': [("Destruction", 'dest', ['destrSubtotal']),
                                 ("Destruction Wait", 'desw', ['deswUTimeAvg']),
                                 ("Vaccination", 'vac', ['vaccVaccination'])]}
    headers = defaultdict(lambda: [('', '', [])], headers)
    headers = headers[model_name]  # select by class
    if prefix:  # filter if there's a prefix
        headers = [item for item in headers if item[1] == prefix]
        title, pref, links = headers[0]
        links = ['/results/' + model_name + '/' + item for item in links]  # otherwise links get broken
        headers[0] = title, pref, links
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
        context['excluded_fields'] = ['zone', 'production_type', 'day', 'iteration', 'id', 'pk', 'last_day']
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



