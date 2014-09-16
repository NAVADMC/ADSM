import os

from django.db import close_old_connections
from django.conf import settings
from django.core.management.base import BaseCommand
import subprocess
from Settings.views import graceful_startup
from git.git import git
from Settings.models import SmSession


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            os.chdir(settings.BASE_DIR)
            graceful_startup()
            session = SmSession.objects.get_or_create()[0]
            if session.update_requested:
                session.update_requested = False
                session.save()
                close_old_connections()

                subprocess.call([git, 'stash'], shell=True)  # trying to get rid of settings.sqlite3 change
                subprocess.call([git, 'reset', '--hard'], shell=True)

                git_status = subprocess.check_output([git, 'pull'], shell=True)
                # TODO: Make sure the pull actually worked
        except:
            print "Failed to update!"
            try:
                subprocess.call([git, 'reset'], shell=True)
                subprocess.call([git, 'stash', 'apply'], shell=True)
            except:
                print "Failed to gracefully reset!"
                return False