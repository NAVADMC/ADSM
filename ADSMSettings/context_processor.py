import re

from ADSMSettings.models import SmSession
from ADSMSettings.models import unsaved_changes
from ADSMSettings.utils import workspace_path, file_list, scenario_filename, npu_update_info


def adsm_context(request):
    context = {}
    if request.path and request.path != '/' and '/LoadingScreen/' not in request.path:
        context = {'filename': scenario_filename(),  # context in either mode
                   'unsaved_changes': unsaved_changes(),
                   'update_available': SmSession.objects.get().update_available,
                   'url': request.path,
                   'active_link': '/'.join(re.split('\W+', request.path)[2:]),
                   'dev_version': 'Current Version',
                   'update_version': 'Newer version',
                   'workspace_path': workspace_path(),
                   'db_files': (file_list(".sqlite3")),
        }

    return context


