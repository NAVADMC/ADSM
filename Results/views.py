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

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
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
    # print('adsm.exe', '-i', iteration_number, 'activeSession.sqlite3', start)
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
    sim = Simulation(OutputSettings.objects.all().first().iterations)
    sim.start()  # starts a new thread
    return render(request, 'Results/SimulationProgress.html', context)


def list_entries(model_name, model, iteration=1):
    return model.objects.filter(iteration=iteration)[:200],


def populate_forms_matching_ProductionType(MyFormSet, TargetModel, context, missing, request):
    """FormSet is pre-populated with existing assignments and it detects and fills in missing
    assignments with a blank form with production type filled in."""


def result_table(request, model_class, model_form):
    """  """
    ResultSet = modelformset_factory(model_class, extra=0, form=model_form)
    context = {'title': 'Results'}
    context['formset'] = ResultSet(queryset=model_class.objects.all())
    return render(request, 'ScenarioCreator/FormSet.html', context)


def model_list(request):
    model_name, model = get_model_name_and_model(request)
    return result_table(request, model, globals()[model_name+'Form'])
    # context = {'title': spaces_for_camel_case(model_name),
    #            'class': model_name,
    #            'name': spaces_for_camel_case(model_name),
    #            'entries': list_entries(model_name, model)}
    # return render(request, 'Results/ResultTable.html', context)

