import threading
from django.shortcuts import render, get_object_or_404, redirect
import subprocess
from Results.models import PingTest


def back_to_inputs(request):
    return redirect('/setup/')


def population(request):
    return redirect('/setup/')


def append_clean_ping(line, ping_objects):
    line = line.decode("utf-8").strip()
    if 'Reply from ' in line:
        print(line)
        ping_objects.append(line)


class Simulation(threading.Thread):
    """execute system commands in a separate thread"""
    def run(self):
        simulation = subprocess.Popen(['ping', 'google.com', '-n', '5'], stdout=subprocess.PIPE)
        ping_lines = []
        while simulation.poll() is None:  # simulation is still running
            append_clean_ping(simulation.stdout.readline(), ping_lines)  # This blocks until it receives a newline.
            if len(ping_lines) > 4:
                PingTest.objects.bulk_create(ping_lines)
                ping_lines = []
        # When the subprocess terminates there might be unconsumed output that still needs to be processed.
        append_clean_ping(simulation.stdout.read(), ping_lines)
        PingTest.objects.bulk_create(ping_lines)


def run_simulation(request):
    context = {'outputs_done': False,}
    sim = Simulation()
    sim.start() # starts a new thread
    return render(request, 'Results/SimulationProgress.html', context)