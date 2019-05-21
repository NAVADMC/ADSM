import os
import re
import time
import shutil
import sqlite3
import multiprocessing

from ADSMSettings.utils import workspace_path, scenario_filename


class CombineOutputsGenerator(multiprocessing.Process):
    import django
    django.setup()

    def __init__(self, **kwargs):
        super(CombineOutputsGenerator, self).__init__(**kwargs)

    def run(self):

        supplemental_location = workspace_path(scenario_filename() + "\\" "Supplemental Output Files" + '\\')  # Note: scenario_filename uses the database
        scenario_name = scenario_filename()
        db_location = workspace_path(scenario_filename() + ".db")

        combine_outputs(supplemental_location, db_location, scenario_name)


def combine_outputs(supplemental_output_folder, db_location, simulation_name):

    all_files = os.listdir(supplemental_output_folder)

    states_files = [file for file in all_files if "states" in file]
    exposures_files = [file for file in all_files if "daily_exposures" in file]
    events_files = [file for file in all_files if "daily_events" in file]

    output_dir = supplemental_output_folder + "Combined Outputs\\"
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        shutil.rmtree(output_dir)
        os.mkdir(output_dir)

    iterations_run = max([len(exposures_files), len(events_files), len(states_files)])

    exposure_days = build_exposures(supplemental_output_folder, exposures_files, output_dir)
    events_days = build_events(supplemental_output_folder, events_files, output_dir)
    states_days = build_states(supplemental_output_folder, states_files, output_dir)

    # days_per_iteration = get_days_from_database(db_location)
    # total_outbreak_days = sum(days_per_iteration)

    file = open(output_dir + "/" + "combined_metadata.txt", "w")

    file.write("Simulation Name: " + simulation_name + "\n")
    file.write("\n")
    file.write("Number of Iterations Run: " + str(iterations_run) + "\n")
    file.write("\n")
    file.write("Total Number of Lines in Exposures Combined Output: " + str(exposure_days) + "\n")
    file.write("Total Number of Lines in Events Combined Output: " + str(events_days) + "\n")
    file.write("Total Number of Lines in States Combined Output: " + str(states_days) + "\n")
    '''
    file.write("\n")
    file.write("Total Outbreak Days: " + str(total_outbreak_days) + "\n")
    file.write("Days in each Iteration:" + "\n")
    for index, iteration in enumerate(days_per_iteration):
        file.write("\t" + "Iteration " + str(index + 1) + ": " + str(iteration) + "\n")
    '''

    file.close()


def get_header(file):
    file = open(file, "r")
    header = file.readlines()[0]
    file.close()
    return header


def build_states(in_path, files, out_path):
    header = get_header(in_path + "/" + files[0])

    data = []

    for file in files:
        next_file = open(in_path + "/" + file, "r")
        new_data = [line.replace("\n", "") for line in next_file.readlines()][1:]
        data += new_data

    file = open(out_path + "/" + "combined_states.csv", "w")
    file.write(header)
    for line in data:
        file.write(line + "\n")
    file.close()

    return len(data) + 1


def build_exposures(in_path, files, out_path):
    header = get_header(in_path + "/" + files[0])

    data = []

    for file in files:
        next_file = open(in_path + "/" + file, "r")
        new_data = [line.replace("\n", "") for line in next_file.readlines()][1:]
        data += new_data

    file = open(out_path + "/" + "combined_daily_exposures.csv", "w")
    file.write(header)
    for line in data:
        file.write(line + "\n")
    file.close()

    return len(data) + 1


def build_events(in_path, files, out_path):
    header = get_header(in_path + "/" + files[0])

    data = []

    for file in files:
        next_file = open(in_path + "/" + file, "r")
        new_data = [line.replace("\n", "") for line in next_file.readlines()][1:]
        data += new_data

    file = open(out_path + "/" + "combined_daily_events.csv", "w")
    file.write(header)
    for line in data:
        file.write(line + "\n")
    file.close()

    return len(data) + 1


'''
def get_days_from_database(database_location):

    db = sqlite3.connect(database_location)
    cursor = db.cursor()
    cursor.execute(
        'SELECT day, last_day, CASE WHEN last_day = "1" THEN "day" ELSE NULL END AS last_day FROM "Results_dailycontrols"'
    )
    daily_controls = cursor.fetchall()
    db.close()

    days_list = []
    for item in daily_controls:
        if item[2]:
            days_list.append(item[2])
    return days_list
'''
