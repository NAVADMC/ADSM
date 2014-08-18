from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future.builtins import zip
from future.builtins import dict
from future.builtins import super
from future.builtins import range
from future.builtins import str
from future import standard_library
standard_library.install_hooks()
from concurrent.futures import ProcessPoolExecutor
from glob import glob
import platform
import threading
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import subprocess
import time
from ScenarioCreator.models import Unit, OutputSettings
from django.db.models import Max
from Results.forms import *  # necessary for globals()[model_name + 'Form']
from Results.models import *  # necessary
import Results.output_parser
from Results.summary import list_of_iterations, summarize_results
import matplotlib
matplotlib.use('Agg')# Force matplotlib to not use any Xwindows backend.
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd


def back_to_inputs(request):
    return redirect('/setup/')


def HttpFigure(fig):
    response = HttpResponse(content_type='image/png')
    FigureCanvas(fig).print_png(response)
    return response


def population_png(request):
    latlong = [(u.latitude, u.longitude) for u in Unit.objects.all()]
    df = pd.DataFrame.from_records(latlong, columns=['Latitude', 'Longitude'])
    axis = df.plot('Longitude', 'Latitude', kind='scatter', color='black', figsize=(4.5, 4))
    return HttpFigure(axis.figure)


def non_empty_lines(line):
    output_lines = []
    line = line.decode("utf-8").strip()
    if len(line):
        output_lines += line.split('\n')  # entries can be more than one line
    return output_lines


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


def breakdown_dictionary(iterate_pt, iterate_zone):
    production_types, zones = {}, {}
    if iterate_pt:
        production_types = dict(ProductionType.objects.all().values_list('name', 'id'))  # Tuples need to be turned into dict
        production_types['All'] = None
    if iterate_zone:
        zones = dict(Zone.objects.all().values_list('name', 'id'))  # Tuples need to be turned into dict
        if iterate_pt:  # Background is only included in DailyByZoneAndProductionType.  See Issue #198
            zones['Background'] = None
    return production_types, zones


def construct_iterating_combination_filter_dictionary(iteration, iterate_pt, iterate_zone):
    """Truth table of iterate_pt and iterate_zone gives you four values.  One for each Daily Model.
    Whether or not iteration is specified raises it to 8 combinations of possible filters used."""
    production_types, zones = breakdown_dictionary(iterate_pt, iterate_zone)
    filter_sequence = []
    columns = ['Day']
    if iteration:  # 1__ Break down lines by production type for only one iteration
        if production_types:  # 11_
            columns += list(production_types.keys())
            if iterate_zone:  # 111
                pass  # TODO: This absolutely needs to only filter one single zone, not iterate_zones for DailyByZoneAndProductionType
            else:  # 110
                for name in production_types.keys():  # add one for each Production Type and "All"
                    filter_sequence.append({'iteration': iteration, 'production_type_id': production_types[name]})
                
        else:  # 10_
            if iterate_zone:  # 101 specific iteration of DailyByZone
                columns += list(zones.keys())
                for name in zones.keys():  # add one for each Zone and "Background"
                    filter_sequence.append({'iteration': iteration, 'zone_id': zones[name]})
            else:  # 100 specific iteration of DailyControl field
                columns.append("Field")
                filter_sequence.append({'iteration': iteration},)  # TODO: Zone=...
            
    else:  # 0__ This is a summary time plot of all iterations.
        columns += ["Iteration " + str(it) for it in list_of_iterations()]  # columns names are always the same,
        # Different graph settings still only get to inject one time line graph per iteration
        biggest_zone = Zone.objects.all().order_by('-radius').first()  # the only "summary" zone stats to be displayed
        for nth_iteration in list_of_iterations():
            if production_types:  # 01_ "All Production Type"
                if iterate_zone:  # 011 "All Production Type" and biggest_zone
                    filter_sequence.append({'iteration': nth_iteration, 'production_type': None, 'zone': biggest_zone})
                else:  # 010
                    filter_sequence.append({'iteration': nth_iteration, 'production_type': None})
                
            else:  # 00_
                if iterate_zone:  #001 DailyByZone
                    filter_sequence.append({'iteration': nth_iteration, 'zone': biggest_zone})
                else:  # 000 DailyControls
                    filter_sequence.append({'iteration': nth_iteration})  

    return filter_sequence, columns


def create_time_series_lines(field_name, model, iterate_pt, iterate_zone, iteration=''):  # Django assigns iteration='' when there's nothing
    filter_sequence, columns = construct_iterating_combination_filter_dictionary(iteration, iterate_pt, iterate_zone)
    lines = []
    for filter_dict in filter_sequence:
        lines.append(list(model.objects.filter(**filter_dict).order_by('day').values_list(field_name, flat=True)))

    return lines, columns


def graph_field_png(request, model_name, field_name, iteration=None):
    model = globals()[model_name]
    iterate_pt, iterate_zone = {"DailyByProductionType": (True, False),
                                "DailyByZoneAndProductionType": (True, True),
                                "DailyByZone": (False, True),
                                "DailyControls": (False, False)}[model_name]

    lines, columns = create_time_series_lines(field_name, model, iterate_pt, iterate_zone, iteration)
    lines.insert(0, list(range(model.objects.all().aggregate(Max('day'))['day__max'])))  # Start with day index

    time_series = zip(*lines)
    time_data = pd.DataFrame.from_records(time_series, columns=columns)  # keys should be same ordering as the for loop above
    time_data = time_data.set_index('Day')
    #TODO: if there are more than 20 iterations, hide or truncate the legend

    fig = plt.figure(figsize=(8, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[4, 1])
    axes = [plt.subplot(gs[0]), ]
    axes.append(plt.subplot(gs[1], sharey=axes[0]))

    time_data.plot(ax=axes[0])
    last_day = time_data.tail(1).T
    last_day.boxplot(ax=axes[1], return_type='axes')
    if len(columns) > 11:
        axes[0].legend().set_visible(False)
    plt.tight_layout()

    return HttpFigure(fig)


def graph_field(request, model_name, field_name, iteration=None):
    if not iteration:
        print("Blank Iteration:", request.path)
    context = {'title': "Graph of %s %s %s" % (model_name, field_name, iteration),
               'image_link': request.path + 'Graph.png'}
    return render(request, 'Results/Graph.html', context)


def empty_fields(model_class, excluded_fields):
    rejected_fields = []
    target_fields = [field for field in model_class._meta.get_all_field_names() if field not in excluded_fields]
    maximums_dict = model_class.objects.all().aggregate(*[Max(field) for field in target_fields])
    for key, value in maximums_dict.items():
        if value is None or value <= 0:
            rejected_fields.append(key[:-5])  # 5 characters in '__max'
    return rejected_fields


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
        context['iterations'] = iterations[:10]  # It's pointless to display links to more than the first 10 iterations, there can be thousands
        context['model_name'] = model_name
        context['excluded_fields'] = ['zone', 'production_type', 'day', 'iteration', 'id', 'pk']
        context['excluded_fields'] += [field for field in model_class._meta.get_all_field_names() if not field.startswith(prefix)]
        context['empty_fields'] = empty_fields(model_class, context['excluded_fields'])
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



