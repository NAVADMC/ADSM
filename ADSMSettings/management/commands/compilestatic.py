import subprocess
import os

from django.core.management import BaseCommand, call_command
from django.conf import settings

from optparse import make_option


class Command(BaseCommand):
    args = "[--option=value, use `compilestatic help` for help]"

    options = None

    option_list = BaseCommand.option_list + (
        make_option('-d', '--dev',
                    action='store_true',
                    dest='dev',
                    default=False,
                    help='Compile with development settings',
                    ),
    )

    def handle(self, *args, **options):
        self.options = options

        if self.options['dev']:
            config_file = 'webpack.config.dev.js'
        else:
            config_file = 'webpack.config.js'

        os.chdir(settings.BASE_DIR)

        command_path = os.path.join('.', 'node_modules', '.bin', 'webpack')
        command = command_path + ' --config %s' % config_file
        webpack = subprocess.Popen(command, cwd=os.path.join(settings.BASE_DIR), shell=True)
        webpack.communicate()  # Wait for webpack to finish compile
        call_command('collectstatic')
