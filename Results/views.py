from concurrent.futures import ProcessPoolExecutor
import threading
from django.forms.models import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import subprocess
import time
from Results.forms import *
from ScenarioCreator.views import get_model_name_and_model
from ScenarioCreator.models import Unit, OutputSettings
from django.db.models import Max

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import pandas as pd


def back_to_inputs(request):
    # TODO: Modal confirmation: "Modifying Inputs will delete any Results created and require you to re-run the simulation"
    return redirect('/setup/')


def HttpFigure(fig):
    response = HttpResponse(content_type='image/png')
    FigureCanvas(fig).print_png(response)
    return response


def population_png(request):
    latlong = [(u.latitude, u.longitude) for u in Unit.objects.all()]
    df = pd.DataFrame.from_records(latlong, columns=['Latitude', 'Longitude'])
    fig = df.plot('Longitude', 'Latitude', kind='scatter', color='black', figsize=(6.5, 6)).figure
    return HttpFigure(fig)


def non_empty_lines(line):
    output_lines = []
    line = line.decode("utf-8").strip()
    if len(line):
        output_lines += line.split('\n')  # entries can be more than one line
    return output_lines


def simulation_process(iteration_number):
    start = time.time()
    simulation = subprocess.Popen(['adsm.exe', '-i', str(iteration_number), 'activeSession.sqlite3'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
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
    return '%i: Success' % iteration_number


class Simulation(threading.Thread):
    """Execute system commands in a separate thread so as not to interrupt the webpage.
    Saturate the computer's processors with parallel simulation iterations"""
    def __init__(self, max_iteration, **kwargs):
        self.max_iteration = max_iteration
        super().__init__(**kwargs)

    def run(self):
        # print(simulation_process())
        statuses = []
        with ProcessPoolExecutor() as executor:
            for exit_status in executor.map(simulation_process, range(1, self.max_iteration+1)):
                statuses.append(exit_status)
        print(statuses)


def run_simulation(request):
    context = {'outputs_done': False}
    delete_all_outputs()
    sim = Simulation(OutputSettings.objects.all().first().iterations)
    sim.start()  # starts a new thread
    return render(request, 'Results/SimulationProgress.html', context)


def list_entries(model_name, model, iteration=1):
    return model.objects.filter(iteration=iteration)[:200],


def list_of_iterations():
    return list(DailyControls.objects.values_list('iteration', flat=True).distinct())


def create_time_series_lines(field_name, model, production_types, iteration=''):  # Django assigns iteration='' when there's nothing
    lines = []
    if iteration:  # Break down lines by production type for only one iteration
        columns = ['Day'] + list(production_types.keys())
        for name in production_types.keys():  # add one for each Production Type and "All"
            lines.append(list(model.objects.filter(iteration=iteration, production_type_id=production_types[name])
                              .order_by('day').values_list(field_name, flat=True)))
    else:  # This is a time plot of all iterations.
        columns = ['Day'] + ["Iteration " + str(it) for it in list_of_iterations()]
        for iteration in list_of_iterations():
            lines.append(list(model.objects.filter(iteration=iteration, production_type=None)  # Only show the "All" Production Type
                              .order_by('day').values_list(field_name, flat=True)))
    return lines, columns


def graph_field_png(request, model_name, field_name, iteration=None):
    model = globals()[model_name]

    production_types = dict(ProductionType.objects.all().values_list('name', 'id'))  # Tuples need to be turned into dict
    production_types['All'] = None
    lines, columns = create_time_series_lines(field_name, model, production_types, iteration)
    lines.insert(0, list(range(model.objects.all().aggregate(Max('day'))['day__max'])))  # Start with day index

    time_series = zip(*lines)
    df = pd.DataFrame.from_records(time_series, columns=columns)  # keys should be same ordering as the for loop above
    df = df.set_index('Day')
    #TODO: if there are more than 20 iterations, hide or truncate the legend
    fig = df.plot(figsize=(6.5, 6)).figure
    return HttpFigure(fig)


def graph_field(request, model_name, field_name, iteration=None):
    if not iteration:
        print("Blank Iteration:", request.path)
    context = {'title': "Graph of %s %s %s" % (model_name, field_name, iteration),
               'image_link': request.path + 'Graph.png'}
    return render(request, 'Results/Graph.html', context)


def result_table(request, model_name, model_class, model_form, graph_links=False):
    """  """
    ResultSet = modelformset_factory(model_class, extra=0, form=model_form)
    context = {'title': 'Results'}
    if not graph_links:
        context['formset'] = ResultSet(queryset=model_class.objects.all().order_by('iteration', 'day')[:50])
        return render(request, 'Results/FormSet.html', context)
    else:
        context['formset'] = ResultSet(queryset=model_class.objects.all().order_by('iteration', 'day')[:5])
        context['Zones'] = Zone.objects.all()
        context['iterations'] = list_of_iterations()[:10]  # It's pointless to display links to more than the first 10 iterations, there can be thousands
        context['model_name'] = model_name
        context['excluded_fields'] = ['production_type', 'day', 'iteration', 'id', 'pk']
        return render(request, 'Results/GraphLinks.html', context)


def model_list(request):
    model_name, model = get_model_name_and_model(request)
    return result_table(request, model_name, model, globals()[model_name+'Form'], True)
    # context = {'title': spaces_for_camel_case(model_name),
    #            'class': model_name,
    #            'name': spaces_for_camel_case(model_name),
    #            'entries': list_entries(model_name, model)}
    # return render(request, 'Results/ResultTable.html', context)

