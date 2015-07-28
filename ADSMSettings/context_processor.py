import os
import re
import subprocess
from ADSMSettings.models import SmSession
from ADSMSettings.models import unsaved_changes
from ADSMSettings.utils import workspace_path, file_list, scenario_filename


def adsm_context(request):
    context = {}
    if request.path and request.path != '/' and '/LoadingScreen/' not in request.path:
        context = {'filename': scenario_filename(),  # context in either mode
                   'unsaved_changes': unsaved_changes(),
                   'update_on_startup': SmSession.objects.get().update_on_startup,
                   'update_available': SmSession.objects.get().update_available,
                   'url': request.path,
                   'active_link': '/'.join(re.split('\W+', request.path)[2:]),
                   'dev_version': npu_update_info(),
                   'update_version': 'Newer version',
                   'workspace_path': workspace_path(),
                   'db_files': (file_list(".sqlite3")),
        }

    return context


def npu_update_info():
    try:
        npu = 'npu.exe'
        npu_response = subprocess.check_output(npu + '--check_update --silent', shell=True, stderr=subprocess.STDOUT).strip()
        print(os.getcwd(), npu_response)
        version = npu_response[-1]
        new_update = version == '1'
        SmSession.objects.all().update(update_available=new_update)
    except:
        version = 'no version information available'
    return version