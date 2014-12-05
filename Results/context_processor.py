from Results.summary import iteration_progress
from Results.views import excluded_headers


def results_context(request):
    context = {}

    if 'results/' in request.path:  # results specific context
        context.update({'results_progress': iteration_progress() * 100,})
        context.update(excluded_headers())

    return context