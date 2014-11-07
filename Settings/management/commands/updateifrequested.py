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
            if session.update_on_startup:
                session.update_available = False
                session.save()
                close_old_connections()

                command = git + ' stash'
                subprocess.call(command, shell=True)  # trying to get rid of settings.sqlite3 change
                command = git + ' reset --hard'
                subprocess.call(command, shell=True)

                command = git + ' pull'
                git_status = subprocess.check_output(command, shell=True)
                # TODO: Make sure the pull actually worked
        except:
            print("Failed to update!")
            try:
                command = git + ' reset'
                subprocess.call(command, shell=True)
                command = git + ' stash apply'
                subprocess.call(command, shell=True)
            except:
                print("Failed to gracefully reset!")
                return False
        finally:
            session = SmSession.objects.get_or_create()[0]
            session.update_on_startup = False
            session.save()