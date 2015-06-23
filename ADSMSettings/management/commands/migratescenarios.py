import os
from django.core.management.base import BaseCommand
from optparse import make_option
import shutil
from django.db import connections, close_old_connections
from django.conf import settings

from ADSMSettings.utils import workspace_path, db_path, graceful_startup
from ADSMSettings.views import open_test_scenario


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--skip-workspace',
                    action='store_true',
                    dest='skip_workspace',
                    default=False,
                    help="Skip migrating scenario files in the user's Workspace folder"),
    )
    
    def handle(self, *args, **options):
        print("Preparing to migrate all Scenario Databases to the current state...")

        current_scenario = db_path(name='scenario_db')
        current_settings = db_path(name='default')
        moved_current = False
        try:
            shutil.move(current_scenario, current_scenario + '.tmp')
            shutil.move(current_settings, current_settings + '.tmp')
            moved_current = True
            print("Backed up current Active Session.")
        except:
            print("Failed to backup current Active Session! Note: it may just not exist which is fine.")

        graceful_startup()

        locations = [os.path.join(settings.BASE_DIR, 'ScenarioCreator', 'tests', 'population_fixtures'), os.path.join(os.path.dirname(settings.BASE_DIR), 'Sample Scenarios'), ]
        if not options['skip_workspace']:
            locations.append(workspace_path())
            print("\nIncluding User's Workspace folder.")
        else:
            print("\nExcluding User's Workspace folder.")

        connections['scenario_db'].close()
        close_old_connections()

        for location in locations:
            for root, dirs, files in os.walk(location):
                for file in files:
                    if file.endswith(".sqlite3") and file != "settings.sqlite3":
                        print("\nMigrating", file, "in", root + "...")
                        try:
                            open_test_scenario(request=None, target=os.path.join(root, file))
                            connections['scenario_db'].close()
                            close_old_connections()
                            shutil.move(db_path('scenario_db'), os.path.join(root, file))
                            print("\nDone.")
                        except Exception as e:
                            print("\nFailed to migrate", file + "!", e)
                            continue
        try:
            if moved_current:
                shutil.move(current_scenario + '.tmp', current_scenario)
                shutil.move(current_settings + '.tmp', current_settings)
                print("Reverted current Active Session.")
        except:
            print("Failed to revert current Active Session!")

        print("Completed migrating all Scenario Databases.")