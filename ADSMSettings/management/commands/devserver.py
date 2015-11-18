from django.core.management import BaseCommand, call_command
from django.conf import settings

import subprocess
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        command_path = os.path.join('.', 'node_modules', '.bin', 'webpack')
        command = command_path + ' --config webpack.config.js --watch'
        webpack = subprocess.Popen(command, cwd=os.path.join(settings.BASE_DIR), shell=True)
        call_command('runserver')
