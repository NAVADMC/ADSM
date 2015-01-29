import re
from ADSMSettings.models import scenario_filename, SmSession
from ADSMSettings.models import unsaved_changes
from ADSMSettings.utils import graceful_startup
from ScenarioCreator.context_processor import git_adsm_sha


def adsm_context(request):
    context = {}
    if request.path != '/' and request.path != '/LoadingScreen/':
        context = {'filename': scenario_filename(),  # context in either mode
                   'unsaved_changes': unsaved_changes(),
                   'update_available': SmSession.objects.get().update_available,
                   'url': request.path,
                   'active_link': '/'.join(re.split('\W+', request.path)[2:]),
                   'dev_version': git_adsm_sha(),
        }
    if 'Scenario/1' in request.path:
        graceful_startup()

    return context