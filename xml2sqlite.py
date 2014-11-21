"""This is simply a command line wrapper for Settings/xml2sqlite.py to avoid a circular import and add
bulk import functionality."""
import os

import sys
import shutil

if __name__ == "__main__":

    print("Preparing Django environment...")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SpreadModel.settings")

    from django.conf import settings
    if not settings.configured:
        settings.configure()
    import django
    django.setup()

    from django.core import management

    from Settings.models import scenario_filename
    from Settings.utils import db_name
    from Settings.views import new_scenario, save_scenario
    from Settings.xml2sqlite import import_naadsm_xml


    if len(sys.argv) == 4:  # single command line invocation
        shutil.copy(db_name(), 'activeSession.bak')
        shutil.copy('settings.sqlite3', 'settings.bak')
        
        new_scenario()
        import_naadsm_xml(sys.argv[1], sys.argv[2])
        scenario_filename(sys.argv[3])
        save_scenario()
        
        shutil.copy('activeSession.bak', db_name())
        shutil.copy('settings.bak', 'settings.sqlite3')
