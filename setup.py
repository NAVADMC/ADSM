from cx_Freeze import setup, Executable
import os

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=[],
                    excludes=["tkinter"],
                    replace_paths=[("*", "")],
                    compressed=False,
                    include_msvcr=True)

base = 'Console'

executables = [
    Executable(os.path.join('src', 'ADSM.py'), base=base, targetName='ADSM.exe'),
    Executable(os.path.join('src', 'ADSM_Update.py'), base=base, targetName='adsm_update.exe'),
]

setup(name='ADSM',
      version='3.2.22',
      description='Animal Disease Spread Model',
      options=dict(build_exe=buildOptions),
      executables=executables)
