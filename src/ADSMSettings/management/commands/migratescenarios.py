import os
from django.core.management.base import BaseCommand
from optparse import make_option
from django.conf import settings
from django.core.management import call_command

from ADSMSettings.utils import workspace_path


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--skip-workspace',
                    action='store_true',
                    dest='skip_workspace',
                    default=False,
                    help="Skip migrating scenario files in the User's Workspace folder"),
    )
    
    def handle(self, *args, **options):
        print("Preparing to migrate all Scenario Databases to the current state...")
        locations = [os.path.join(settings.BASE_DIR, 'ScenarioCreator', 'tests', 'population_fixtures'), os.path.join(os.path.dirname(settings.BASE_DIR), 'Sample Scenarios'), ]
        if not options['skip_workspace']:
            locations.append(workspace_path())
            print("Including User's Workspace folder.")
        else:
            print("Excluding User's Workspace folder.")

        for location in locations:
            for root, dirs, files in os.walk(location):
                for file in files:
                    if file.endswith(".sqlite3") and file != "settings.sqlite3":
                        print("Migrating", file, "in", root + "...")
                        settings.DATABASES['temp_migration'] = {
                            'NAME': os.path.join(root, file),
                            'ENGINE': 'django.db.backends.sqlite3',
                            'OPTIONS': {
                                'timeout': 300,
                            }
                        }
                        call_command('migrate', database='temp_migration', interactive=False)
                        print("Done.")

        try:
            del(settings.DATABASES['temp_migration'])
        except:
            print("Failed to remove temp_migration database from settings!")

        print("Completed migrating all Scenario Databases.")