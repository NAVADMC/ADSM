from django.db import close_old_connections
from django.core.management.base import BaseCommand
from ADSMSettings.models import SmSession
from ADSMSettings.utils import update_requested
from git.git import update_adsm


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        try:
            if update_requested():
                print("It has been requested to run an update...")
                if update_adsm():
                    session = SmSession.objects.get_or_create()[0]
                    session.update_available = False
                    session.save()
        except:
            pass
        finally:
            try:
                session = SmSession.objects.get_or_create()[0]
                session.update_on_startup = False
                session.save()
            except:
                print("Failed to gracefully reset!")
                return False
            finally:
                close_old_connections()
