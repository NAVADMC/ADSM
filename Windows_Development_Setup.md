Setting Up ADSM for Development Work in Windows
==========

Setup Python Environment
----------

Install External Dependencies:

  - Python 3.4.2 (x64): https://www.python.org/ftp/python/3.4.2/python-3.4.2.amd64.msi
  - Git: https://git-scm.com/download/win
    - Make sure it is on your PATH
  - Visual Studio 2010: http://download.microsoft.com/download/D/B/C/DBC11267-9597-46FF-8377-E194A73970D6/vs_proweb.exe
    - Note: Installing the trial is fine as all we need is the compiler. Where VS the GUI App may stop working after 30 days, the CLI compiler should continue to be valid
  - Node LTS x64: https://nodejs.org/dist/v6.9.1/node-v6.9.1-x64.msi
  - Nullsoft Scriptable Install System (version shouldn't matter): http://nsis.sourceforge.net/Download

Once Python3.4 is installed, you will need to create a Virtual Environment for the ADSM Project.  
This is important, especially if you plan on compiling a distributable version, as we will package the Virtual Environment to send off with the deployable.  
So make sure that your Virtual Environment is dedicated to this project and clean of unneeded package installations.

Create Virtual Environment:

  - Run: `DRIVE:\\path\to\python3.4\python -m venv DRIVE:\\path\to\adsm_venv`
  - Modify File: 'DRIVE:\\path\to\python3.4\Lib\distutils\msvc9compiler.py'
    - Note: This file is not in your venv, but in your base Python3.4 install
    - After 'ld_args.append('/MANIFESTFILE:' + temp_manifest)' add 'ld_args.append('/MANIFEST')' at the same indentation level
  - Activate with: `DRIVE:\\path\to\adsm_venv\Scripts\activate.bat`
  - Confirm the venv is active with `where pip` and `where python`. Both should be listed as in your adsm_venv Scripts directory
  - Confirm that NO packages from your global install made it into your Virtual Environment. Use `pip freeze` to confirm nothing is installed
  - In the ADSM folder: `pip install -r Requirements.txt`
  - Download all the Wheel (*.whl) files located here: https://newline.us/ADSM/setup/
  - install numpy: `pip install numpy-1.9.3+mkl-cp34-none-win_amd64.whl`
  - install matplotlib: `pip install matplotlib-1.4.3-cp34-none-win_amd64.whl`
  - install pandas: `pip install pandas-0.15.2-cp34-none-win_amd64.whl`
  - install scipy: `pip install scipy-0.15.1-cp34-none-win_amd64.whl`
  - install pyproj: `pip install pyproj-1.9.4-cp34-none-win_amd64.whl`
  - install psutil: `pip install psutil-2.2.1-cp34-none-win_amd64.whl`
  - Download PyWin32 from: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win-amd64-py3.4.exe/download
  - install PyWin32: `DRIVE:\\path\to\adsm_venv\Scripts\easy_install.exe pywin32-219.win-amd64-py3.4.exe`
  - `pip install cx_freeze==4.3.4`
  - Modify File: 'DRIVE:\\path\to\adsm_venv\Lib\site-packages\cx_Freeze\finder.py'
    - Make the changes outlined in this patch: https://bitbucket.org/BryanHurst/cx_freeze/commits/eba6cb644d390f69f07adbf9fdcead71ec0feebf?at=default
  - In the ADSM folder: `npm install`
  - Download: http://chromedriver.storage.googleapis.com/2.12/chromedriver_win32.zip
  - Unzip chromedriver and place it in 'DRIVE:\\path\to\adsm_venv\Scripts\'
  
Development and Production Branches
-----------

List of Relevant Branches: master, Stable

Development should be done in feature branches and merged into master. Master is the general development branch, and where Beta releases come from.

Stable is the branch we merge master into when we are ready to do a production release.  
**Stable branch is what will be tagged in the GitHub Releases.**    
Master is tagged in GitHub as pre-release.

During Development
----------
During Development, it would be a pain to continually build the project just for testing.  
Thankfully, this is a Python project and so does not actually need to be compiled to run if you have the Virtual Environment setup.

Just like if you were to install ADSM on a server for hosting cloud services, you don't need a compiled distributable.

To run ADSM locally in development mode, use `DRIVE\\path\to\adsm_venv\Scripts\python.exe manage.py devserver`.  
This is slightly different from Django's normal `runserver` as it also launches a separate webpack process to compile any React client elements.


Updating the Distributable
----------

When releasing a Beta compile from Master Branch:

  - Bump the version in `ADSM/__init__.py` and in `package.json`. See the [Version Guide](https://github.com/NAVADMC/ADSM/wiki/Version-Guide) for the meaning of the four parts of the version number.
  - Build (with sourced python) `python setup.py build`
  - Push the Update `cd build` `npu.exe --create_update --program=ADSM_Beta --program_id=PROGRAM_ID --password=PASSWORD` You can find the program ID and password by logging into the Newline Program Updater (everyone authorized to create releases will have a login).
  - Update the latest pre-release with a new tag (don't change the release title)
  - Create a zip file of your build directory to attach to the GitHub release
  
When releasing a Production compile from Stable Branch:

  - Bump the version in `ADSM/__init__.py`, in `package.json` and in `installer_windows.nsi`. See the [Version Guide](https://github.com/NAVADMC/ADSM/wiki/Version-Guide) for the meaning of the four parts of the version number.
  - Build (with sourced python) `python setup.py build`
  - Push the Update `cd build` `npu.exe --create_update --program=ADSM --program_id=PROGRAM_ID --password=PASSWORD` You can find the program ID and password by logging into the Newline Program Updater (everyone authorized to create releases will have a login). 
  - Update the latest release with a new tag (don't change the release title)
  - Run the nsi script ('installer_windows.nsi') with the Nullsoft Scriptable Install System and upload the output to the releaseon GitHub