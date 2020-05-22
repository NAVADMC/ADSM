import auto_runner

from django.core.management import BaseCommand


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

    def handle(self, *args, **options):
        auto_runner.setup(options)
        return
