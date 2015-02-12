import os
import shutil
import zipfile
from django.shortcuts import redirect

import psutil

from ADSMSettings.models import scenario_filename, SimulationProcessRecord
from ADSMSettings.utils import workspace_path, supplemental_folder_has_contents


def is_simulation_running():
    return len(get_simulation_controllers()) > 0


def get_simulation_controllers():
    results = []
    records = SimulationProcessRecord.objects.all()  # really shouldn't be longer than 1
    for record in records:
        for process in psutil.process_iter():
            if process.pid == record.pid:
                if 'python' not in process.name().lower() and 'adsm' not in process.name().lower():
                    record.delete()  # stale process record where the pid was reused
                else:  # process call python
                    results.append(process)
    return results


def delete_supplemental_folder():
    scenario_folder = scenario_filename()
    if scenario_folder != '':
        try:
            shutil.rmtree(workspace_path(scenario_folder))
        except:
            pass  # because the folder doesn't exist (which is fine)

        from django.db import connections
        connections['scenario_db'].cursor().execute('VACUUM')
        

def map_zip_file():
    """This is a file named after the scenario in the folder that's also named after the scenario."""
    return workspace_path(scenario_filename() + '/' + scenario_filename() + " Map Output.zip")


def zip_map_directory_if_it_exists():
    dir_to_zip = workspace_path(scenario_filename() + "/Map")
    if os.path.exists(dir_to_zip) and supplemental_folder_has_contents(subfolder='/Map'):
        zipname = map_zip_file()
        dir_to_zip_len = len(dir_to_zip.rstrip(os.sep)) + 1
        with zipfile.ZipFile(zipname, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            for dirname, subdirs, files in os.walk(dir_to_zip):
                for filename in files:
                    path = os.path.join(dirname, filename)
                    entry = path[dir_to_zip_len:]
                    zf.write(path, entry)
    else:
        print("Folder is empty: ", dir_to_zip)


def abort_simulation(request=None):
    for process in get_simulation_controllers():
        print("Aborting Simulation Thread")
        process.kill()
    if request is not None:
        return redirect('/results/')


def delete_all_outputs():
    from Results.models import DailyControls, DailyReport, DailyByZone, DailyByProductionType, DailyByZoneAndProductionType, UnitStats, ResultsVersion
    abort_simulation()
    if DailyControls.objects.count() > 0:
        print("DELETING ALL OUTPUTS")
    for model in [DailyControls, DailyReport, DailyByZone, DailyByProductionType, DailyByZoneAndProductionType, UnitStats, ResultsVersion]:
        model.objects.all().delete()

