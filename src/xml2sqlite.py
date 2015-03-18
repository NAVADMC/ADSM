"""This is simply a command line wrapper for Settings/xml2sqlite.py to avoid a circular import and add
bulk import functionality."""
import os

import sys
import shutil

if __name__ == "__main__":

    print("Preparing Django environment...")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")

    from django.conf import settings
    import django
    django.setup()

    from django.core import management

    from ADSMSettings.models import scenario_filename
    from ADSMSettings.utils import db_path, workspace_path
    from ADSMSettings.views import new_scenario, save_scenario
    from ADSMSettings.xml2sqlite import import_naadsm_xml
    from ScenarioCreator.models import DirectSpread


    if len(sys.argv) >= 4:  # single command line invocation
        print("""Usage: python3.4 ./xml2sqlite.py export_pop.xml parameters.xml debug.sqlite3 [workspace]
        Include the word 'workspace' as the fourth if you want to save the scenario to the ADSM Workspace""")
        shutil.copy(db_path(), workspace_path('activeSession.bak'))
        shutil.copy(db_path('default'), workspace_path('settings.bak'))
        
        popul_path = sys.argv[1]
        param_path = sys.argv[2]
        scenario_path = workspace_path(sys.argv[3]) if len(sys.argv) > 4 and sys.argv[4] == 'workspace' else sys.argv[3]
        scenario_name = os.path.basename(scenario_path)
        new_scenario()
        import_naadsm_xml(popul_path, param_path, saveIterationOutputsForUnits=False)
        scenario_filename(scenario_name)
        save_scenario()
        print("DirectSpread.objects.count()", DirectSpread.objects.count())

        shutil.move(workspace_path(scenario_name), scenario_path)
        
        shutil.copy(workspace_path('activeSession.bak'), db_path())
        shutil.copy(workspace_path('settings.bak'), db_path('default'))

