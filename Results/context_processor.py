from Results.summary import iteration_progress
from Results.views import excluded_headers
from Results.utils import is_simulation_running


def results_context(request):
    context = {}

    if 'results/' in request.path:  # results specific context
        context.update({'results_progress': iteration_progress() * 100,
                        'is_simulation_running': is_simulation_running(),
        })
        context.update(excluded_headers())

    return context