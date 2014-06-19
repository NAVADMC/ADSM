from concurrent.futures import ProcessPoolExecutor
import threading
from django.shortcuts import render, get_object_or_404, redirect
import subprocess
from Results.models import PingTest


def back_to_inputs(request):
    # Modal confirmation: "Modifying Inputs will delete any Results created and require you to re-run the simulation"
    return redirect('/setup/')


def population(request):
    return redirect('/setup/')


def append_clean_ping(line, ping_objects):
    line = line.decode("utf-8").strip()
    if 'Reply from ' in line:
        print(line)
        ping_objects.append(line)


def run_iteration(iteration_number):
    print("Running", iteration_number)
    simulation = subprocess.Popen(['ping', 'nyx', '-n', '5'], stdout=subprocess.PIPE)
    ping_lines = []
    while simulation.poll() is None:  # simulation is still running
        append_clean_ping(simulation.stdout.readline(), ping_lines)  # This blocks until it receives a newline.
        if len(ping_lines) > 900:
            PingTest.objects.bulk_create(ping_lines)
            ping_lines = []
    # When the subprocess terminates there might be unconsumed output that still needs to be processed.
    append_clean_ping(simulation.stdout.read(), ping_lines)
    PingTest.objects.bulk_create(ping_lines)
    return '%i: Success' % iteration_number


class Simulation(threading.Thread):
    """execute system commands in a separate thread so as not to interrupt the webpage.
    Saturate the computer's processors with parallel simulation iterations"""
    def run(self):
        with ProcessPoolExecutor() as executor:
            exit_statuses = executor.map(run_iteration, list(range(5)))
            print(exit_statuses)


def run_simulation(request):
    context = {'outputs_done': False,}
    sim = Simulation()
    sim.start() # starts a new thread
    return render(request, 'Results/SimulationProgress.html', context)