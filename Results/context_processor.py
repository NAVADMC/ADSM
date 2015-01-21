import threading
from Results.summary import iteration_progress
from Results.views import excluded_headers


def results_context(request):
    context = {}

    if 'results/' in request.path:  # results specific context
        context.update({'results_progress': iteration_progress() * 100,
                        'simulation_running': any([thread.name == 'simulation_control_thread' for thread in threading.enumerate()]),
        })
        context.update(excluded_headers())

    return context