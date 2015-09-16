from ADSMSettings.models import SmSession
from Results.summary import iteration_progress, iterations_complete
from Results.views import excluded_headers
from Results.models import outputs_exist, ResultsVersion
from Results.utils import is_simulation_running, is_simulation_stopped


def results_context(request):
    context = {}
    
    if 'results/' in request.path or 'setup/' in request.path:  # results specific context
        session = SmSession.objects.get()
        context.update({'simulation_has_started': session.simulation_has_started,
                        'outputs_exist': outputs_exist(),
                        'results_progress': iteration_progress() * 100,})

        try:
            version = ResultsVersion.objects.all().first().__str__()  # singleton doesn't always work on this model (legacy)
        except:
            version = "No version available"
        context.update({
                        'is_simulation_running': is_simulation_running(),
                        'is_simulation_stopped': is_simulation_stopped(),
                        'iterations_completed': iterations_complete(),
                        'version_number': version
    
        })
        context.update(excluded_headers())

    return context