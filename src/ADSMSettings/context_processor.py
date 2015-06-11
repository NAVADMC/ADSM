import re
from ADSMSettings.models import scenario_filename, SmSession
from ADSMSettings.models import unsaved_changes
from ADSMSettings.utils import graceful_startup, workspace_path, file_list
from ScenarioCreator.context_processor import git_adsm_sha


def adsm_context(request):
    context = {}
    if 'Scenario/1' in request.path:
        graceful_startup()
    if request.path != '/' and request.path != '/LoadingScreen/':
        context = {'filename': scenario_filename(),  # context in either mode
                   'unsaved_changes': unsaved_changes(),
                   'update_on_startup': SmSession.objects.get().update_on_startup,
                   'update_available': SmSession.objects.get().update_available,
                   'url': request.path,
                   'active_link': '/'.join(re.split('\W+', request.path)[2:]),
                   'dev_version': git_adsm_sha(),
                   'workspace_path': workspace_path(),
                   'db_files': (file_list(".sqlite3")),
        }

    return context