"""Utility Views for UI 
Leave this code here until we can use it for importing chunks of a scenario in the Scenario Builder"""

import os
from ADSM import settings


def create_db_connection(db_name, db_path):
    from django.db import connections
    needs_sync = not os.path.isfile(db_path)

    connections.databases[db_name] = {
        'NAME': os.path.join(settings.BASE_DIR, db_path),
        'ENGINE': 'django.db.backends.sqlite3'}
    # Ensure the remaining default connection information is defined.
    # EDIT: this is actually performed for you in the wrapper class __getitem__
    # method.. although it may be good to do it when being initially setup to
    # prevent runtime errors later.
    # connections.databases.ensure_defaults(db_name)
    if needs_sync:
        # Don't import django.core.management if it isn't needed.
        from django.core.management import call_command
        print('Building DB structure...')
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")
        call_command('migrate',
            # verbosity=0,
            interactive=False,
            database=db_name,
            fake_initial=True)  # connections.databases[db_name].alias,  # database=self.connection.alias,
        print('Done creating database')


# def db_save(file_path):
#     create_db_connection('save_file', file_path)
#     top_level_models = [Scenario, Population, Disease, VaccinationGlobal]
#     for parent_object in top_level_models:
#         try:
#             node = parent_object.objects.using('default').get()
#             node.save(using='save_file')
#         except ObjectDoesNotExist:
#             print("Couldn't find a ", parent_object)
# 
#     unsaved_changes(False)  # File is now in sync
#     return 'Scenario Saved'