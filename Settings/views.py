from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
import os
import subprocess
from django.conf import settings
from django.shortcuts import redirect


def update_adsm_from_git(request):
    git = os.path.join(settings.BASE_DIR, 'git', 'bin', 'git.exe')
    subprocess.call(git + ' reset --hard', shell=True)
    subprocess.call(git + ' pull', shell=True)
    return redirect('/setup/')


def update_is_needed():
    git = os.path.join(settings.BASE_DIR, 'git', 'bin', 'git.exe')
    subprocess.call(git + ' remote update', shell=True)
    status = subprocess.call(git + ' status -uno', shell=True)
    return 'behind' in status
