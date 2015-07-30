import re

from ADSMSettings.models import SmSession
from ADSMSettings.models import unsaved_changes
from ADSMSettings.utils import workspace_path, file_list, scenario_filename, npu_update_info

from ADSM import __version__


def adsm_context(request):
    context = {}
    if request.path and request.path != '/' and '/LoadingScreen/' not in request.path:
        version = SmSession.objects.get().update_available
        context = {'filename': scenario_filename(),  # context in either mode
                   'unsaved_changes': unsaved_changes(),
                   'url': request.path,
                   'active_link': '/'.join(re.split('\W+', request.path)[2:]),
                   'dev_version': __version__,
                   'update_version': version if version and version != 'False' else '',
                   'workspace_path': workspace_path(),
                   'db_files': (file_list(".sqlite3")),
        }

    return context


