import os

from django.db import close_old_connections
from django.conf import settings
from django.core.management.base import BaseCommand
from Settings.views import graceful_startup
from Settings.models import SmSession
from Settings.utils import update_adsm


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            os.chdir(settings.BASE_DIR)
            graceful_startup()
            session = SmSession.objects.get_or_create()[0]
            if session.update_on_startup:
                print("It has been requested to run an update...")
                session.update_available = False
                session.save()
                close_old_connections()

                update_adsm()
        except:
            pass
        finally:
            try:
                session = SmSession.objects.get_or_create()[0]
                session.update_on_startup = False
                session.save()
            except:
                pass
            close_old_connections()
