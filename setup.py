import sys
import os
import pip
import shutil

from cx_Freeze import setup, Executable, build_exe
from importlib import import_module

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ADSM.settings")
import django
django.setup()
from django.conf import settings
from django.core import management

from ADSM import __version__


build_exe_options = {
    'build_exe': 'build',
    'optimize': 2,
    'excludes': [
        # CHANGE ME for any python packages in your project that you want excluded
        'development_scripts',
    ],
    'includes': [

    ],
    'packages': [
        # Known missing Python imports.
        # This may need to be updated from time to time as new projects uncover more missing packages.
        'html',
        'shutil',
    ],
    'replace_paths': [('*', '')],
    'compressed': False,
    'include_files': [
        # Standard Django items to bring in
        ('static', 'static'),
        ('media', 'media'),
        ('bin', 'bin'),
        ('Viewer', 'Viewer'),  # Newline's View application for Django Desktop Core
        ('npu.exe', 'npu.exe'),  # Newline's Program Updater application  # TODO: This is windows specific

        # CHANGE ME for any files/folders you want included with your project
        ('Sample Scenarios', 'Sample Scenarios'),
        ('Database Templates', 'Database Templates')
    ],
    'include_msvcr': True  # CHANGE ME depending on if your project has licensing that is compatible with Microsoft's redistributable license
}


def query_yes_no(question, default='yes'):
    valid = {'yes': True, 'y': True, "no": False, 'n': False}

    if default is None:
        prompt = " [y/n] "
    elif default in ['yes', 'y']:
        prompt = " [Y/n] "
    elif default in ['no', 'n']:
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer!")

    while True:
        sys.stdout.write('\n' + question + prompt)

        choice = input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'.\n")


def get_packages_in_path(path):
    packages = []
    for folder in os.listdir(path):
        if os.path.exists(os.path.join(path, folder, '__init__.py')):
            packages.extend([folder, ])
        elif folder.endswith('.egg') and not os.path.isfile(os.path.join(path, folder)):
            for subfolder in os.listdir(os.path.join(path, folder)):
                if os.path.exists(os.path.join(path, folder, subfolder, '__init__.py')):
                    packages.extend([subfolder, ])
    return packages


def get_installed_packages():
    site_packages = pip.util.site_packages

    return get_packages_in_path(site_packages)


def get_local_packages():
    return get_packages_in_path(settings.BASE_DIR)


def remove_empty_folders(path):
    if not os.path.isdir(path):
        return

    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                remove_empty_folders(fullpath)

    files = os.listdir(path)
    if len(files) == 0:
        print("Removing empty folder:", path)
        os.rmdir(path)


class BuildADSM(build_exe):
    def run(self):
        print("\nYou should only run this build script if you are a CLEAN VirtualEnv!\n"
              "The VirtualEnv will be deployed with the project, "
              "so make sure it ONLY has the REQUIRED dependencies installed!")
        if not query_yes_no("Are you in a CLEAN Python Environment?", default='no'):
            sys.exit()

        if not os.path.exists(os.path.join(settings.BASE_DIR, 'static')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'static'))
        management.call_command('collectstatic', interactive=False, clear=True)
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'media')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'media'))

        management.call_command('migratescenarios', skip_workspace=True)
        management.call_command('makeresultsurls')
        management.call_command('makescenariocreatorurls')

        shutil.rmtree(os.path.join(settings.BASE_DIR, self.build_exe), ignore_errors=True)

        # Grab all the packages that we should include (local and those installed in the virtualenv)
        self.packages.extend(get_installed_packages())
        self.packages.extend(get_local_packages())
        # Cleanup packages to account for any excludes
        self.packages = [package for package in self.packages
                                         if package not in self.excludes]

        # Grab any templates or translation files for installed apps and copy those
        for app_name in settings.INSTALLED_APPS:
            app = import_module(app_name)
            if os.path.exists(os.path.join(app.__path__[0], 'templates')):
                self.include_files.extend([(os.path.join(app.__path__[0], 'templates'),
                                                            os.path.join('templates', app.__name__)), ])
            # TODO: Do we need to grab translation files for apps not listed in settings.py?
            # TODO: Django still doesn't properly find translation for domain 'django' after collecting everything
            # if os.path.exists(os.path.join(app.__path__[0], 'locale')):
            #     build_exe_options['include_files'].extend([(os.path.join(app.__path__[0], 'locale'),
            #                                                 os.path.join('locale', app.__name__)), ])

        # Check all installed packages and see if they list any dependencies they need copied when frozen
        for package in self.packages:
            try:
                package = import_module(package)
                if getattr(package, '__include_files__', False):
                    self.include_files.extend(package.__include_files__)
            except Exception as e:
                print("Error bringing in dependent files!", str(e), "This is probably okay.")
                continue

        build_exe.run(self)

        files = (file for file in os.listdir(os.path.join(settings.BASE_DIR, self.build_exe))
                 if os.path.isfile(os.path.join(settings.BASE_DIR, self.build_exe, file)))
        os.makedirs(os.path.join(settings.BASE_DIR, self.build_exe, 'bin', 'env'))
        for file in files:
            if file not in ['ADSM.exe', 'ADSM_Beta.exe', 'library.zip', 'python34.dll', 'MSVCR100.dll', 'npu.exe']:  # TODO: This line is ADSM specific
                shutil.move(os.path.join(settings.BASE_DIR, self.build_exe, file),
                            os.path.join(settings.BASE_DIR, self.build_exe, 'bin', 'env', file))


base = None
if sys.platform == 'win32':
    base = 'Console'  # TODO: Change to Win32GUI and so on for each OS

cmdclass = {"build_exe": BuildADSM, }

setup(name='ADSM Beta',
      version=__version__,
      description='ADSM Beta Application',
      options={'build_exe': build_exe_options,
               'install_exe': {'build_dir': build_exe_options['build_exe']}},
      executables=[Executable('ADSM.py', base=base, targetName='ADSM_Beta.exe'), ],  # TODO: Icon goes in Executable
      cmdclass=cmdclass,
      )  # TODO: install_requires should read in the requirements files per os

# Cleanup step after any sort of setup operation
# TODO: See if this causes issues at the end of an 'install' command.
# If so, override the msi build command and put this at the end of the normal build and the installer build
remove_empty_folders(os.path.join(settings.BASE_DIR, build_exe_options['build_exe']))