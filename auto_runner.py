from ADSM import settings


def setup(args):
    """ Setup the auto-runner. This function mainly is in place to handle the exclude-file, if one is given.

    :param args: list of command line arguments
    :return: None
    """

    # string to hold the name of the exclude file
    exclude_file_name = ""
    # string to hold the location of the scenarios to auto-run
    scenarios_path = ""
    # file var to hold to exclude file object
    exclude_file = None
    # variable denoting if additional print statements should be used or not
    verbose = False

    print("Auto-run mode detected, setting up...")

    # for every index and argument in the given arguments
    for index, arg in enumerate(args):
        # if the current argument denotes that the next will be the scenarios path
        if arg == "--scenarios-path":
            # set the scenarios_path variable
            scenarios_path = args[index+1]
        # if the current argument denotes that the next will be an exclude file
        if arg == "--exclude-file":
            # set the exclude file name
            exclude_file_name = args[index+1]
        if arg == "-v":
            verbose = True

    if verbose:
        print(("[setup] Given exclude-file name is: " + exclude_file_name) if exclude_file_name != "" else
              "[setup] No exclude-file name detected.")
        print(("[setup] Given scenarios-path is: " + scenarios_path) if scenarios_path != "" else
              "[setup] No scenarios-path given, defaulting to the ADSM working directory.")

    # if no scenario_path was given
    if scenarios_path == "":
        # get the default path from settings
        scenarios_path = settings.WORKSPACE_PATH

        if verbose:
            print("[setup] Detected ADSM working directory is: ", scenarios_path)

    # test if an exclude file was given before trying to open it
    if exclude_file_name != "":
        # we're going to try to catch if the file could not be opened
        try:
            if verbose:
                print("[setup] Opening exclude file...")
            exclude_file = open(exclude_file_name, "r")
            if verbose:
                print("[setup] File opened.")
        except FileNotFoundError:
            # print an error message
            print("\n\nGIVEN EXCLUDE FILE COULD NOT BE OPENED")
            if verbose:
                print("[setup] aborting ADSM")
            # exit ADSM
            return None
    # if no exclude file name was given
    else:
        # let the user know one was not detected. This is printed so if the user intended to have an exclude file
        # but their arguments had a typo they know that their exclude file was not used.
        print("No exclude file given, running all scenarios in current working directory.")

    if verbose:
        print("[setup] Setup complete, starting ADSM auto-runner.")
    # call the run function (with the opened exclude file, or None), this will actually start the auto-run process.
    run(exclude_file if exclude_file is not None else None, verbose)

    if verbose:
        print("[setup] ADSM auto-runner complete, cleaning up...")

    # if an exclude file was opened
    if exclude_file is not None:
        if verbose:
            print("[setup] Closing the exclude file.")
        # close it
        exclude_file.close()

    if verbose:
        print("[setup] Clean up complete. Closing ADSM.")
    # exit ADSM
    return None


def run(scenarios_path, exclude_file=None, verbose=False):
    """ auto-run main function. Loops through file in the current working directory and hands them to execute_next to
    actually run them through the simulator.

    :param scenarios_path: file path to a folder containing the scenarios the user wishes to run.
    :param exclude_file: file object with list of scenarios to skip
    :param verbose: boolean denoting if additional print statements should be output
    :return: None
    """
    return None


def execute_next(next_scenario_name, verbose=False):
    """ This function takes a single scenario name from the current ADSM working directory and runs that scenario
    through the simulator.

    :param next_scenario_name: scenario name to run
    :param verbose: boolean denoting if additional print statements should be output
    :return: 0 if scenario executed as expected, 1 if an error occured.
    """
    return