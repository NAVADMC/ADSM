import multiprocessing
import subprocess
import platform
import sqlite3
import time
import os

from django.core.management import BaseCommand
from ADSM import settings


class Command(BaseCommand):
    help = "Run the ADSM auto scenario runner."

    def add_arguments(self, parser):
        parser.add_argument('--verbose', dest='verbose',
                            help='Output extra status updates to the terminal.', action='store_true')
        parser.add_argument('--run-all-scenarios', dest='run_all_scenarios',
                            help='Start the auto runner without any excluded scenarios.', action='store_true')
        parser.add_argument('--exclude-scenarios', dest='exclude_scenarios',
                            help='A list of scenarios to exclude from the auto runner.', nargs='+')
        parser.add_argument('--exclude-scenarios-list', dest='exclude_scenarios_list',
                            help="Filename that contains scenario names to exclude, one per line.", action='store')
        parser.add_argument('--run-scenarios', dest='run_scenarios',
                            help='A list of scenarios to auto run.', nargs="+")
        parser.add_argument('--run-scenarios-list', dest='run_scenarios_list',
                            help='Filename that contains scenario names to run, one per line.', action='store')
        parser.add_argument('--workspace-path', dest='workspace_path',
                            help="Give a different workspace path to pull scenarios from.", action='store')
        parser.add_argument('--max-iterations', dest='max_iterations',
                            help="Maximum number of iterations any single simulation can run.", action='store')

    def handle(self, *args, **options):
        setup(options)
        return


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
    # boolean to mark if a scenario from the workspace should be used or not
    include = False

    print("\nAuto-run mode detected, setting up...")

    # check and make sure that a command line arguments conflict was not given by the user
    if args["run_all_scenarios"] and \
            (args["run_scenarios"] is not None or args["run_scenarios_list"] is not None):
        raise InvalidArgumentsGiven('"run-all-scenarios" cannot be used with either '
                                    '"run-scenarios" or "run-scenarios-list".')

    # make sure that a valid max_iterations argument was given
    try:
        # make sure it exists in the first place before we try and convert it to an integer
        if args["max_iterations"] is not None:
            # make the conversion
            args["max_iterations"] = int(args["max_iterations"])
    except ValueError:
        raise InvalidArgumentsGiven("The given iterations max could not be converted to an integer.")

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

        # if additional specific scenario names were given to include
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
                    # next we'll check to make sure that a DO.NOT.RUN file is also not in the scenario directory

                    # get all of the files within the potential scenario
                    potential_files = os.listdir(args["workspace_path"] + "/" + file)

                    # if a DO.NOT.RUN file is in the scenario
                    if "DO.NOT.RUN" not in potential_files:
                        # for each file within the potential scenarios
                        for db_file in potential_files:
                            # if that file name has the .db extension
                            if ".db" in db_file:
                                if args["verbose"]:
                                    print("\t[setup] Scenario confirmed, adding to list of known scenarios")
                                scenarios.append(db_file.replace(".db", ""))
                                break
                        else:
                            raise ScenarioConflict("A given scenario was both included and excluded.")
                    else:
                        raise ScenarioConflict("A given scenario was both included and excluded.")
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

                # if a DO.NOT.RUN file is in the scenario
                if "DO.NOT.RUN" not in potential_files:
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
    # loop through all of the given scenarios
    for scenario in args["scenarios"]:
        print("\nRunning next scenario: \"" + scenario + "\"")
        execute_next(args, args["workspace_path"] + "\\" + scenario)

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


def execute_next(args, scenario):
    """ This function takes a single scenario path and runs that scenario through the simulator.

    :param args: dictionary of parameters
    :param scenario: Path to scenario to run through the simulator
    :return: 0 if scenario executed as expected, 1 if an error occurred.
    """

    # string to the path of the .db file within the scenario
    db_file = ""

    if args["verbose"]:
        print("\t[execute] Full path of next scenario to be run: " + scenario)

    for file in os.listdir(scenario):
        if ".db" in file:
            db_file = file
            break

    if args["verbose"]:
        print("\t[execute] Scenario Database File: " + db_file)

    # Get the actual number of iterations to run from the scenario itself
    # open the scenario for reading
    db_conn = sqlite3.connect(os.path.abspath(os.path.join(scenario, db_file)))
    db_curr = db_conn.cursor()

    # execute the query
    db_curr.execute("SELECT iterations from ScenarioCreator_outputsettings")

    # actually save the value (fetchone() returns a tuple)
    args["next_iterations_count"] = int(db_curr.fetchone()[0])

    db_conn.close()

    # Make sure that said scenarios iterations count is not more than the max (if a user max was specified)
    if args["max_iterations"] is not None:
        if args["next_iterations_count"] > args["max_iterations"]:
            args["next_iterations_count"] = args["max_iterations"]

    if args["verbose"]:
        print("\t[execute] Running", args["next_iterations_count"], "iteration(s).")
        print("\t[execute] Starting Simulation...")

    # create the simulation object
    sim = Simulation(args, scenario_path=os.path.abspath(os.path.join(scenario, db_file)))
    # run the simulation
    sim.start()

    if args["verbose"]:
        print("\t[execute] Simulation Complete.")

    print("Done.")

    return


def simulation_process(iteration_number, adsm_cmd, log_path):
    start = time.time()

    simulation = subprocess.Popen(adsm_cmd,
                                  shell=(platform.system() != "Darwin"),
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  bufsize=1)
    simulation.communicate()

    end = time.time()

    return iteration_number, end - start


class Simulation(multiprocessing.Process):
    def __init__(self, args: dict, scenario_path="activeSession.db", **kwargs):
        super(Simulation, self).__init__(**kwargs)
        self.args = args
        self.scenario_path = scenario_path

    def run(self):

        try:

            sim_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                    "..", "..", "..", "bin"))
            num_cores = multiprocessing.cpu_count()
            # if num_cores > 2:  # Standard processor saturation
            #     num_cores -= 1
            if num_cores > 3:  # Lets you do other work while running sims
                num_cores -= 2
            executable_cmd = [os.path.join(sim_path, 'adsm_simulation.exe'), self.scenario_path,
                              '--output-dir', os.path.join(sim_path, 'Supplemental-Output-Files')]

            statuses = []
            pool = multiprocessing.Pool(num_cores)
            for iteration in range(1, self.args["next_iterations_count"] + 1):
                adsm_cmd = executable_cmd + ['-i', str(iteration)]
                res = pool.apply_async(func=simulation_process, args=(iteration, adsm_cmd, sim_path))
                statuses.append(res)

            pool.close()

            simulation_times = []
            for status in statuses:
                iteration_number, s_time = status.get()
                simulation_times.append(round(s_time))

        except (BaseException, Exception):
            raise


class InvalidArgumentsGiven(Exception):
    pass


class ScenarioConflict(Exception):
    pass
