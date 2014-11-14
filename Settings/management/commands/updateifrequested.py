from django.db import close_old_connections
from django.core.management.base import BaseCommand
from Settings.models import SmSession
from Settings.utils import update_adsm, update_requested


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
