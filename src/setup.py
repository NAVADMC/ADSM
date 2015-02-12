from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=[],
                    excludes=["tkinter"],
                    replace_paths=[("*", "")],
                    compressed=False,
                    include_msvcr=True)

base = 'Console'

executables = [
    Executable('ADSM.py', base=base, targetName='ADSM.exe'),
    Executable('ADSM_Update.py', base=base, targetName='adsm_update.exe'),
    Executable('ADSM_Force_Reset_and_Update.py', base=base, targetName='adsm_force_reset_and_update.exe')
]

setup(name='ADSM',
      version='3.2.22',
      description='Animal Disease Spread Model',
      options=dict(build_exe=buildOptions),
      executables=executables)
