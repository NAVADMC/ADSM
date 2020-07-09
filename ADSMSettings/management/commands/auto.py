import json
import shutil
import subprocess
import platform
import os
import sys

from django.conf import settings
from django.core.management import BaseCommand
from django.db import close_old_connections
from djanto.utils import timezone as djtimezone

from ADSMSettings.utils import adsm_executable_command, graceful_startup
from ADSMSettings.views import open_scenario
from Results.simulation import Simulation
from Results.utils import delete_all_outputs, delete_supplemental_folder
from Results.views import create_blank_unit_stats
from ScenarioCreator.models import DestructionGlobal, OutputSettings
from ScenarioCreator.views import match_data


class Command(BaseCommand):
    help = "Run the ADSM Auto Scenario Runner."

    scenarios = []  # List of all scenarios to process
    options = None
    log_file = None

    def add_arguments(self, parser):
        parser.add_argument('--run-all-scenarios', dest='run_all_scenarios',
                            help='Run all Scenarios in the Workspace with the ADSM Auto Scenario Runner unless a file called DO.NOT.RUN is present in the scenario folder.', action='store_true')
        parser.add_argument('--exclude-scenarios', dest='exclude_scenarios',
                            help='A list of scenarios to exclude from the ADSM Auto Scenario Runner. Ex: "Scenario 1" "Scenario 2"', nargs='+')
        parser.add_argument('--exclude-scenarios-list', dest='exclude_scenarios_list',
                            help="File that contains a list of scenario names to exclude from the ADSM Auto Scenario Runner, one per line.", action='store')
        parser.add_argument('--run-scenarios', dest='run_scenarios',
                            help='A list of scenarios for the ADSM Auto Scenario Runner to run. Ex: "Scenario 1" "Scenario 2"', nargs="+")
        parser.add_argument('--run-scenarios-list', dest='run_scenarios_list',
                            help='File that contains a list of scenario scenario names to run with the ADSM Auto Scenario Runner, one per line.', action='store')
        parser.add_argument('--store-logs', dest='store_logs',
                            help='Should logs from each Scenario be saved? Default is to the current working directory unless output-path is defined.', action='store_true')
        parser.add_argument('--workspace-path', dest='workspace_path',
                            help="Give a different workspace path to pull scenarios from for the ADSM Auto Scenario Runner.", action='store')
        parser.add_argument('--output-path', dest='output_path',
                            help="Where the ADSM Auto Scenario Runner should store output logs.", action='store')
        parser.add_argument('--max-iterations', dest='max_iterations',
                            help="Maximum number of iterations any single simulation can run with the ADSM Auto Scenario Runner.", action='store')
        parser.add_argument('--quiet', dest='quiet',
                            help='Skip all user prompts and automatically reply Yes.', action='store_true')

    def handle(self, *args, **options):
        self.options = options

        if not self.options['workspace_path'] and not self.options['quiet']:
            print("WARNING! Using the ADSM Auto Scenario Runner will cause you to lose any unsaved work in the Scenario currently open in ADSM (activeSession.db). Please make sure all current changes are saved back to your Scenario in the ADSM program.")
            print()
            print("WARNING! Using the ADSM Auto Scenario Runner will delete existing Results and Supplemental Output Files on all scenarios that are run.")
            print()
            print("Are you okay with losing any unsaved work and existing results?")

            answer = None
            while str(answer).lower() not in ['yes', 'y', 'no', 'n']:
                answer = str(input('Enter (Y)es or (N)o: ')).lower()
                if answer in ['yes', 'y']:
                    break
                elif answer in ['no', 'n']:
                    print('\nYou may either open the ADSM Program and save the current Scenario, or you may specify a custom Workspace with "--workspace-path" to avoid conflict with the ADSM Program.')
                    return
                else:
                    print("Unknown input!")

        if not self.options['output_path']:
            self.options['output_path'] = '.'
        else:
            os.makedirs(self.options['output_path'], exist_ok=True)

        with open(os.path.join(self.options['output_path'], 'auto_output.log'), 'w') as self.log_file:
            self.setup_scenarios()
            self.run_scenarios()

        return

    def log(self, message):
        print(message)
        self.log_file.write("\n%s" % message)

    def setup_scenarios(self):
        self.log("\nADSM Auto Scenario Runner mode detected, setting up...\n")
        # check and make sure that a command line arguments conflict was not given by the user
        if self.options["run_all_scenarios"] and (self.options["run_scenarios"] is not None or self.options["run_scenarios_list"] is not None):
            raise InvalidArgumentsGiven('The argument "run-all-scenarios" cannot be used with either "run-scenarios" or "run-scenarios-list"!')

        # make sure that a valid max_iterations argument was given
        try:
            # make sure it exists in the first place before we try and convert it to an integer
            if self.options["max_iterations"] is not None:
                # make the conversion
                self.options["max_iterations"] = int(self.options["max_iterations"])
        except ValueError:
            raise InvalidArgumentsGiven('The given "max_iterations" could not be converted to an integer!')
        if self.options["max_iterations"] is not None and self.options['max_iterations'] <= 0:
            raise InvalidArgumentsGiven('The given "max_iterations" must be greater than 0!')

        # Setup the workspace path
        if self.options["workspace_path"] is None:
            self.options["workspace_path"] = settings.WORKSPACE_PATH
        else:
            self.options['workspace_path'] = os.path.abspath(self.options['workspace_path'])

        if not getattr(sys, 'frozen', False):  # This is preempted in ADSM.py when compiled
            if os.path.exists(settings.AUTO_SETTINGS_FILE):
                os.remove(settings.AUTO_SETTINGS_FILE)

            settings.WORKSPACE_PATH = self.options['workspace_path']
            settings.DB_BASE_DIR = os.path.join(settings.WORKSPACE_PATH, "settings")
            settings.DATABASES.update({
                'default': {
                    'NAME': os.path.join(settings.DB_BASE_DIR, 'settings.db'),
                    'ENGINE': 'django.db.backends.sqlite3',
                    'TEST': {'NAME': os.path.join(settings.DB_BASE_DIR, 'test_settings.db')},
                },
                'scenario_db': {
                    'NAME': os.path.join(settings.DB_BASE_DIR, 'activeSession.db'),
                    'ENGINE': 'django.db.backends.sqlite3',
                    'TEST': {'NAME': os.path.join(settings.DB_BASE_DIR, 'test_activeSession.db')},
                    'OPTIONS': {
                        'timeout': 300,
                    }
                }
            })
            with open(settings.AUTO_SETTINGS_FILE, 'w') as user_settings:
                user_settings.write('WORKSPACE_PATH = %s' % json.dumps(settings.WORKSPACE_PATH))

        if not os.path.isdir(self.options['workspace_path']):
            raise InvalidArgumentsGiven('"workspace_path" not found!')

        close_old_connections()
        graceful_startup(skip_examples=True, skip_updates=True)
        os.makedirs(os.path.join(settings.DB_BASE_DIR, "logs"), exist_ok=True)

        # tab here because this will actually line up with the argument summary above
        self.log("\nScenarios will be pulled from the following Workspace: %s" % self.options["workspace_path"])

        self.log("Building complete scenario list...")
        if self.options['run_all_scenarios'] or (not self.options['run_scenarios'] and not self.options['run_scenarios_list']):
            for root, dirs, files in os.walk(self.options['workspace_path']):
                for dir in dirs:
                    if dir not in ['Example Database Queries', 'Example R Code', 'settings']:
                        dir_files = os.listdir(os.path.join(self.options['workspace_path'], dir))
                        for file in dir_files:
                            if file.endswith('.db'):
                                self.scenarios.append(file)
                                break  # Don't add a directory more than once
                break  # only look at the top level for folders that may contain DBs

        # Compile formatted include and exclude scenario lists
        include_scenarios = []
        exclude_scenarios = []

        if self.options['run_scenarios']:
            for scenario in self.options['run_scenarios']:
                if not str(scenario).lower().endswith('.db'):
                    scenario = "%s.db" % scenario
                include_scenarios.append(scenario)
        if self.options['run_scenarios_list']:
            with open(self.options['run_scenarios_list'], 'r') as scenarios:
                for scenario in scenarios:
                    scenario = scenario.strip()
                    if not str(scenario).lower().endswith('.db'):
                        scenario = "%s.db" % scenario
                    include_scenarios.append(scenario)

        if self.options['exclude_scenarios']:
            for scenario in self.options['exclude_scenarios']:
                if not str(scenario).lower().endswith('.db'):
                    scenario = "%s.db" % scenario
                exclude_scenarios.append(scenario)
        if self.options['exclude_scenarios_list']:
            with open(self.options['exclude_scenarios_list'], 'r') as scenarios:
                for scenario in scenarios:
                    scenario = scenario.strip()
                    if not str(scenario).lower().endswith('.db'):
                        scenario = "%s.db" % scenario
                    exclude_scenarios.append(scenario)

        if set(include_scenarios) & set(exclude_scenarios):
            raise ScenarioConflict("A given Scenario was both included and excluded!")

        for scenario in include_scenarios:
            if scenario not in self.scenarios:
                self.scenarios.append(scenario)
        if exclude_scenarios:
            self.scenarios = [scenario for scenario in self.scenarios if scenario not in exclude_scenarios]
        do_not_run = []
        for scenario in self.scenarios:
            if os.path.exists(os.path.join(self.options['workspace_path'], scenario.replace('.db', ''), 'DO.NOT.RUN')):
                do_not_run.append(scenario)
        if do_not_run:
            self.scenarios = [scenario for scenario in self.scenarios if scenario not in do_not_run]

        self.log("\tRunning the following scenarios: %s" % ', '.join(self.scenarios))

    def run_scenarios(self):
        self.log("\nSetup complete, starting ADSM Auto Scenario Runner...")

        for scenario in self.scenarios:
            self.log("\nAuto running %s..." % scenario)

            open_scenario(None, scenario, wrap_target=True)
            print("Starting Simulation run at %s" % djtimezone.now())
            delete_all_outputs()
            delete_supplemental_folder()
            create_blank_unit_stats()  # create UnitStats before we risk the simulation writing to them

            # ensure that the destruction_reason_order includes all elements. See #990 for more details
            dg = DestructionGlobal.objects.all().first()
            if dg:
                DestructionGlobal.objects.filter(pk=1).update(destruction_reason_order=match_data(dg.destruction_reason_order, "Basic, Trace fwd direct, Trace fwd indirect, Trace back direct, Trace back indirect, Ring"))

            self.log("\tValidating simulation setup...")
            simulation = subprocess.Popen(adsm_executable_command() + ['--dry-run'],
                                          shell=(platform.system() != 'Darwin'),
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
            stdout, stderr = simulation.communicate()  # still running while we work on python validation
            simulation.wait()  # simulation will process db then exit
            if simulation.returncode == 0 and not stderr:
                self.log("\tPASSED")
            else:
                self.log("\tFAILED! Skipping Scenario %s" % scenario)
                continue

            if not self.options['max_iterations']:
                try:
                    max_iterations = OutputSettings.objects.all().first().iterations
                except:
                    print("Unable to find OutputSettings! Scenario may not be complete or is corrupt. Skipping Scenario %s" % scenario)
                    continue
            else:
                max_iterations = self.options['max_iterations']

            self.log("\tRunning simulation...")
            sim = Simulation(max_iteration=max_iterations)
            sim.start()
            sim.join()  # Wait for it to complete
            if self.options['store_logs']:
                log_dir = os.path.join(self.options['workspace_path'], 'settings', 'logs')
                scenario_output = os.path.join(self.options['output_path'], "%s Auto Output" % scenario.replace(".db", ""))
                os.makedirs(scenario_output, exist_ok=True)
                for f in os.listdir(log_dir):
                    shutil.move(os.path.join(log_dir, f), os.path.join(scenario_output, f))
            self.log("\tDone running %s." % scenario)

        self.log("\nDone running all Scenarios.")


class InvalidArgumentsGiven(Exception):
    pass


class ScenarioConflict(Exception):
    pass
