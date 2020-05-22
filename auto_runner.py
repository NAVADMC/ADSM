from itertools import chain
from ADSM import settings
from glob import glob

import os


def setup(args):
    """ Setup the auto-runner. This function mainly is in place to handle the exclude-file, if one is given.

    :param args: argsparse arguments object
    :return: None
    """

    # list of all scenarios to process, not filled if args.run_scenarios has any values
    scenarios = []
    # list of scenarios to exclude
    excluded_scenarios = []
    # file containing names of scenarios to exclude, one per line
    exclude_file = None
    # list of scenarios to include
    included_scenarios = []
    # file containing names of scenarios to include, one per line
    include_file = None
    file_text = ""  # raw file data

    print("\nAuto-run mode detected, setting up...")
    print(args)
    print(args["run_all_scenarios"])

    # check and make sure that a command line arguments conflict was not given by the user
    if args["run_all_scenarios"] and \
            (args["run_scenarios"] is not None or args["run_scenarios_list"] is not None):
        raise InvalidArgumentsGiven('"run-all-scenarios" cannot be used with either '
                                    '"run-scenarios" or "run-scenarios-list".')

    if args["verbose"]:
        print("[setup] Argument Summary: ")
        print("\t[setup] Running all scenarios (unless manually excluded)"
              if args["run_all_scenarios"] else
              "\t[setup] Only running specified scenarios.")
        print(("\t[setup] Excluded scenarios: " + str(args["exclude_scenarios"]))
              if args["exclude_scenarios"] is not None else
              "\t[setup] No specific scenarios excluded.")
        print(("\t[setup] Given exclude-file name is: " + args["exclude_scenarios_list"])
              if args["exclude_scenarios_list"] is not None else
              "\t[setup] No exclude-file name detected.")
        print(("\t[setup] Scenarios included to be run: " + str(args["run_scenarios"]))
              if args["run_scenarios"] is not None else
              "\t[setup] No specific scenario included.")
        print(("\t[setup] Given include-file name is: " + args["run_scenarios_list"])
              if args["run_scenarios_list"] is not None else
              "\t[setup] No include-file name detected.")

    # if no scenario_path was given
    if args["workspace_path"] is None:
        # get the default path from settings
        args["workspace_path"] = settings.WORKSPACE_PATH

        if args["verbose"]:
            # tab here because this will actually line up with the argument summary above
            print("\t[setup] Scenarios will be pulled from this directory: ", args["workspace_path"])
    else:
        # tab here because this will actually line up with the argument summary above
        print("\t[setup] Scenarios will be pulled from this directory: ", args["workspace_path"])

    if args["verbose"]:
        print("\n[setup] Building complete scenario exclusion list...")

    # test if an exclude file was given before trying to open it
    if args["exclude_scenarios_list"] is not None:
        # we're going to try to catch if the file could not be opened
        try:
            if args["verbose"]:
                print("\t[setup] Opening exclude file...")
            exclude_file = open(args["exclude_scenarios_list"], "r")
            if args["verbose"]:
                print("\t[setup] File opened.")
        except FileNotFoundError:
            # print an error message
            print("\n\nGIVEN EXCLUDE-SCENARIOS-LIST FILE COULD NOT BE OPENED")
            if args["verbose"]:
                print("[setup] aborting ADSM")
            # exit ADSM
            return None

    # first we need to create a list of excluded scenarios
    # if an exclude_file was even given
    if exclude_file is not None:
        # get the file data
        file_text = exclude_file.readlines()
        # build the exclusion list be removing newlines
        excluded_scenarios = [file_name.replace("\n", "") for file_name in file_text]

    if args["verbose"] and args["exclude_scenarios_list"] is not None:
        print("\t[setup] " + str(len(excluded_scenarios)) + " scenario(s) were collected from the given file.")

    # if additional specific scenario names were given to exclude
    if args["exclude_scenarios"] is not None:
        # append those scenarios to the excluded_scenarios list
        excluded_scenarios += args["exclude_scenarios"]
        if args["verbose"]:
            print("\t[setup] " + str(len(args["exclude_scenarios"])) +
                  " scenario(s) were collected from the command line.")

    if args["verbose"]:
        print("[setup] Excluded scenarios compiled: " + str(excluded_scenarios) +
              "\t(Duplicate scenarios names will not cause any errors.)")
        print("\n[setup] Building complete scenario inclusion list...")

    # we don't need to collect any of the included scenarios if the --run-all-scenarios option was given
    if not args["run_all_scenarios"]:

        # test if an include file was given before trying to open it
        if args["run_scenarios_list"] is not None:
            # we're going to try to catch if the file could not be opened
            try:
                if args["verbose"]:
                    print("\t[setup] Opening include file...")
                include_file = open(args["run_scenarios_list"], "r")
                if args["verbose"]:
                    print("\t[setup] File opened.")
            except FileNotFoundError:
                # print an error message
                print("\n\nGIVEN RUN-SCENARIOS-LIST FILE COULD NOT BE OPENED")
                if args["verbose"]:
                    print("[setup] aborting ADSM")
                # exit ADSM
                return None

        # first we need to create a list of included scenarios
        # if an include_file was even given
        if include_file is not None:
            # get the file data
            file_text = include_file.readlines()
            # for each file name
            for file in file_text:
                # get rid of that pesky newline
                file.replace("\n", "")
                # check and make sure that name is not also in the exluded list
                if file in excluded_scenarios:
                    raise ScenarioConflict("A given scenario was both included and excluded.")
                else:
                    included_scenarios.append(file)

        if args["verbose"] and args["run_scenarios_list"] is not None:
            print("\t[setup] " + str(len(included_scenarios)) + " scenario(s) were collected from the given file.")

        # if additional specific scenario names were given to exclude
        if args["run_scenarios"] is not None:
            # we need to check and make sure each included file is also not excluded
            # for each file name
            for file in args["run_scenarios"]:
                # get rid of that pesky newline
                file.replace("\n", "")
                # check and make sure that name is not also in the excluded list
                if file in excluded_scenarios:
                    raise ScenarioConflict("A given scenario was both included and excluded.")
                else:
                    included_scenarios.append(file)

            if args["verbose"]:
                print("\t[setup] " + str(len(args["run_scenarios"])) +
                      " scenario(s) were collected from the command line.")
    else:
        if args["verbose"]:
            print("\t[setup] Collecting scenarios from the workspace...")

        # for every folder in the given workspace
        for potential in os.listdir(args["workspace_path"]):
            if args["verbose"]:
                print("\n\t[setup] Checking next potential scenario: " + potential)

            # make sure the potential is not excluded, no sense verifying it if we can't use it anyways
            if potential in excluded_scenarios:
                if args["verbose"]:
                    print("\t[setup] Potential scenario excluded by user. Skipping.")
                continue

            # try catch block will prevent anything not a directory in the workspace from stopping ADSM
            try:
                # get all of the files within the potential scenario
                potential_files = os.listdir(args["workspace_path"] + "/" + potential)

                # hard-check to make sure we're not in the settings folder
                if 'activeSession.db' in potential_files and 'settings.db' in potential_files:
                    if args["verbose"]:
                        print("\t[setup] Settings folder detected. Skipping.")
                    continue

                # for each file within the potential scenarios
                for file in potential_files:
                    # if that file name has the .db extension
                    if ".db" in file:
                        if args["verbose"]:
                            print("\t[setup] Scenario confirmed, adding to list of known scenarios")
                        scenarios.append(potential)
                        break
                else:
                    if args["verbose"]:
                        print("\t[setup] Scenario denied.")
            except NotADirectoryError:
                if args["verbose"]:
                    print("\t[setup] Potential is not a directory. Skipping.")
                continue

    if args["verbose"]:
        print("\n[setup] Included scenarios compiled:", scenarios,
              "\t(Excluded scenarios have already been removed from this list.)\n")

    args["scenarios"] = scenarios

    print("Setup complete, starting ADSM auto-runner.")

    # call the run function (with the opened exclude file, or None), this will actually start the auto-run process.
    run(args)

    if args["verbose"]:
        print("\n[setup] ADSM auto-runner complete, cleaning up...")

    # if an exclude file was opened
    if "exclude_file" in args.keys():
        if args["verbose"]:
            print("[setup] Closing the exclude file.")
        # close it
        exclude_file.close()

    if args["verbose"]:
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


class InvalidArgumentsGiven(Exception):
    pass


class ScenarioConflict(Exception):
    pass
