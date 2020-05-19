from CSUtils import args2dict
from itertools import chain
from ADSM import settings
from glob import glob

import os


def setup(args):
    """ Setup the auto-runner. This function mainly is in place to handle the exclude-file, if one is given.

    :param args: list of command line arguments
    :return: None
    """

    # dictionary of the arguments
    parsed_args = {}
    # file object for the exclude file
    exclude_file = ""
    # list of all scenarios to process
    scenarios = []
    # list of scenarios to exclude (if applicable)
    excluded_scenarios = []
    file_text = ""  # raw file data

    # parse the given arguments into that dictionary
    parsed_args = args2dict(args)

    # if the arguments could not be parsed
    if parsed_args is None:
        # exit program
        print("\nInvalid command line arguments given.")
        return None

    # if the verbose flag was not given
    if "v" not in parsed_args.keys():
        # set it to false
        parsed_args["v"] = False

    print("\nAuto-run mode detected, setting up...")

    if parsed_args["v"]:
        print(("[setup] Given exclude-file name is: " + parsed_args["exclude_file"])
              if "exclude_file" in parsed_args.keys() else
              "[setup] No exclude-file name detected.")
        print(("[setup] Given scenarios-path is: " + parsed_args["scenarios_path"])
              if "scenarios_path" in parsed_args.keys() else
              "[setup] No scenarios-path given, defaulting to the ADSM working directory.")

    # if no scenario_path was given
    if "scenarios_path" not in parsed_args.keys():
        # get the default path from settings
        parsed_args["scenarios_path"] = settings.WORKSPACE_PATH

        if parsed_args["v"]:
            print("[setup] Detected ADSM working directory is: ", parsed_args["scenarios_path"])

    # test if an exclude file was given before trying to open it
    if "exclude_file" in parsed_args.keys():
        # we're going to try to catch if the file could not be opened
        try:
            if parsed_args["v"]:
                print("[setup] Opening exclude file...")
            exclude_file = open(parsed_args["exclude_file"], "r")
            if parsed_args["v"]:
                print("[setup] File opened.")
        except FileNotFoundError:
            # print an error message
            print("\n\nGIVEN EXCLUDE FILE COULD NOT BE OPENED")
            if parsed_args["v"]:
                print("[setup] aborting ADSM")
            # exit ADSM
            return None
    # if no exclude file name was given
    else:
        # let the user know one was not detected. This is printed so if the user intended to have an exclude file
        # but their arguments had a typo they know that their exclude file was not used.
        print("No exclude file given, running all scenarios.")

    if parsed_args["v"]:
        print("[setup] Building list of scenarios to run...")

    # first we need to create a list of excluded scenarios
    # if an exclude_file was even given
    if exclude_file is not None:
        # get the file data
        file_text = exclude_file.readlines()
        # build the exclusion list be removing newlines
        excluded_scenarios = [file_name.replace("\n", "") for file_name in file_text]

    # for every folder in the given workspace
    for potential in os.listdir(parsed_args["scenarios_path"]):
        if parsed_args["v"]:
            print("\n[setup] Checking next potential scenario: " + potential)

        # make sure the potential is not excluded, no sense verifying it if we can't use it anyways
        if potential in excluded_scenarios:
            if parsed_args["v"]:
                print("[setup] Potential scenario excluded by user. Skipping.")
            continue

        # try catch block will prevent anything not a directory in the workspace from stopping ADSM
        try:
            # get all of the files within the potential scenario
            potential_files = os.listdir(parsed_args["scenarios_path"] + "/" + potential)

            # hard-check to make sure we're not in the settings folder
            if 'activeSession.db' in potential_files and 'settings.db' in potential_files:
                if parsed_args["v"]:
                    print("[setup] Settings folder detected. Skipping.")
                continue

            # for each file within the potential scenarios
            for file in potential_files:
                # if that file name has the .db extension
                if ".db" in file:
                    if parsed_args["v"]:
                        print("[setup] Scenario confirmed, adding to list of known scenarios")
                    scenarios.append(potential)
                    break
            else:
                if parsed_args["v"]:
                    print("[setup] Scenario denied.")
        except NotADirectoryError:
            if parsed_args["v"]:
                print("[setup] Potential is not a directory. Skipping.")
            continue

    if parsed_args["v"]:
        print("\n[setup] Collected scenarios:", scenarios, "\n")

    parsed_args["scenarios"] = scenarios

    print("Setup complete, starting ADSM auto-runner.")

    # call the run function (with the opened exclude file, or None), this will actually start the auto-run process.
    run(parsed_args)

    if parsed_args["v"]:
        print("\n[setup] ADSM auto-runner complete, cleaning up...")

    # if an exclude file was opened
    if "exclude_file" in parsed_args.keys():
        if parsed_args["v"]:
            print("[setup] Closing the exclude file.")
        # close it
        exclude_file.close()

    if parsed_args["v"]:
        print("[setup] Clean up complete. Closing ADSM.")
    # exit ADSM
    return None


def run(options):
    """ auto-run main function. Loops through file in the current working directory and hands them to execute_next to
    actually run them through the simulator.

    A scenario is defined as a folder within the given scenarios_path that has at least (but not exclusively) at .db
    file within. The exception to this is the "settings" folder withing the default ADSM workspace, which contains
    multiple .db files but is not considered a scenario.

    :param options: dictionary of formatted parameters
    :return: None
    """

    # loop through all of the given scenarios
    for scenario in options["scenarios"]:
        print("Running next scenario: \"" + scenario + "\"")

    return None


def execute_next(options, exclude_file):
    """ This function takes a single scenario name from the current ADSM working directory and runs that scenario
    through the simulator.

    :param options: dictionary of formatted parameters
    :param exclude_file: file object with a list of scenarios to skip (one scenario per line)
    :return: 0 if scenario executed as expected, 1 if an error occurred.
    """
    return
