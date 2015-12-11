import subprocess
import os

from django.core.management import BaseCommand, call_command
from django.conf import settings

from optparse import make_option


class Command(BaseCommand):
    args = "[--option=value, use `devserver help` for help]"

    options = None

    option_list = BaseCommand.option_list + (
        make_option('-d', '--dev',
                    action='store_true',
                    dest='dev',
                    default=False,
                    help='Run development settings',
                    ),
    )

    def handle(self, *args, **options):
        self.options = options

        if self.options['dev']:
            config_file = 'webpack.config.dev.js'
        else:
            config_file = 'webpack.config.js'

        command_path = os.path.join('.', 'node_modules', '.bin', 'webpack')
        command = command_path + ' --config %s --watch' % config_file
        webpack = subprocess.Popen(command, cwd=os.path.join(settings.BASE_DIR), shell=True)
        call_command('runserver')
