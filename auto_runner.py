from ADSM import settings
from CSUtils import args2dict


def setup(args):
    """ Setup the auto-runner. This function mainly is in place to handle the exclude-file, if one is given.

    :param args: list of command line arguments
    :return: None
    """

    # dictionary of the arguments
    parsed_args = {}
    # file object for the exclude file
    exclude_file = ""

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

    print("Setup complete, starting ADSM auto-runner.")

    # call the run function (with the opened exclude file, or None), this will actually start the auto-run process.
    run(parsed_args, exclude_file)

    if parsed_args["v"]:
        print("[setup] ADSM auto-runner complete, cleaning up...")

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


def run(options, exclude_file):
    """ auto-run main function. Loops through file in the current working directory and hands them to execute_next to
    actually run them through the simulator.

    :param options: dictionary of formatted parameters
    :param exclude_file: file object with a list of scenarios to skip (one scenario per line)
    :return: None
    """
    return None


def execute_next(options, exclude_file):
    """ This function takes a single scenario name from the current ADSM working directory and runs that scenario
    through the simulator.

    :param options: dictionary of formatted parameters
    :param exclude_file: file object with a list of scenarios to skip (one scenario per line)
    :return: 0 if scenario executed as expected, 1 if an error occurred.
    """
    return