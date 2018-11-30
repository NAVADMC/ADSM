# ADSM (Animal Disease Spread Model)
A Frontend application with Desktop and Web Based GUI for creating a simulation model to assist decision making and education in evaluating animal disease incursions.  

Project Owner - Missy Schoenbaum, USDA:APHIS:VS:CEAH Modeling Team contact melissa.schoenbaum@aphis.usda.gov

This repo is the primary repo for the ADSM project and houses the main Frontend that users will be interacting with.  
It creates scenarios by storing their parameters in a SQLite file and displays results after running a simulation.  
A more detailed breakdown of this application will follow.

## Installing ADSM As An End User
ADSM can be installed on either x86-64 Windows 7 - 10 or x86-64 Debian based Linux Systems (Ubuntu preferred).  
There is a Beta and Release channel available for installation.

### Windows Release Channel
You can find the latest Release here: https://github.com/NAVADMC/ADSM/releases/latest

1. On the latest release page, download the "ADSM_Installer.exe".
1. Run the installer with admin privileges (ask your IT department for help if needed).
1. Follow the on screen prompts until "Choose Install Location".
1. Choose the folder in which to install ADSM. This is where the program will reside. It is generally best to put it in "Program Files".
1. Next, choose the User Workspace Folder for ADSM. If you are the only user of the computer, you can choose where to store your Workspace Folder (folder of your scenarios). Note that you must have Read/Write access to the chosen folder.  
   If ADSM is being installed on a shared computer and multiple users will use the program, leave this field BLANK so ADSM will find a suitable Workspace Folder that is writable and unique to each user.
1. Continue following the on screen prompts.
1. When installation is complete, find "ADSM.exe" (either a shortcut on your desktop or in the folder you installed ADSM) and run it.
1. After launching the application, a black Terminal window with white text will appear. You can leave this window alone; some debug messages may appear in it.
1. A Viewer window will then appear on top of the Terminal window. This is where you will interface with the ADSM program.
1. To properly exit ADSM, close the Viewer window. Doing so will automatically close the Terminal window after saving and shutting down all processes.

### Debian Linux Release Channel
You can find the latest Release here: https://github.com/NAVADMC/ADSM/releases/latest

An installation process does not yet exist for Linux, so it is best for each user on a machine to download their own local copy of the program.

1. On the latest release page, download the "ADSM.tar.gz".
1. Extract the package into the folder in which you want ADSM to be installed. It is best to do this somewhere in your User space.
1. Run the "ADSM" executable in the extracted folder.
1. After launching the application, a Terminal will appear. You can leave this Terminal alone; some debug messages may appear in it.
1. A Viewer window will then appear on top of the Terminal window. This is where you will interface with the ADSM program.
1. To properly exit ADSM, close the Viewer window. Doing so will automatically close the Terminal after saving and shutting down all processes.

### Windows And Linux Beta Channel
You can find the latest Pre-release on the Releases page: https://github.com/NAVADMC/ADSM/releases

Beta builds do not come with an installer, so it is best for each user on a machine to download their own local copy of the program.

**WARNING:** If you have a Release installation on your computer, the Beta install MAY **overwrite your scenarios** from the Release version if you didn't specify a custom Workspace directory during Release install.   
If ADSM is selecting the Workspace directory automatically both the Release and Beta channel will select the same folder.

1. On the latest pre-release page, download either "ADSM_vx.x.x.x-beta_windows.zip" or "ADSM_vx.x.x.x-beta_linux.tar.gz"
1. Extract the package into the folder in which you want ADSM Beta to be installed. It is best to do this somewhere in your User space (a directory your user owns).
1. If you need to specify a different Workspace Folder to avoid a conflict with a Production Release, follow these steps.
   1. In your ADSM Beta folder, create a file called "settings.ini".
   1. Using your favorite text editor, add one of the following lines:
      1. Windows: `WORKSPACE_PATH = 'DRIVE:\\desired\\path\\to\ADSM Beta Workspace'`
      1. Linux: `WORKSPACE_PATH = '/desired/path/to/ADSM Beta Workspace'`  
1. Run the "ADSM_Beta.exe" or "ADSM_Beta" executable in the extracted folder.
1. After launching the application, a Terminal will appear. You can leave this Terminal alone; runtime and debug messages will appear in it.
1. A Viewer window will then appear on top of the Terminal window. This is where you will interface with the ADSM Beta program.
1. To properly exit ADSM Beta, close the Viewer window. Doing so will automatically close the Terminal after saving and shutting down all processes.

### Installing ADSM On A Server (Cloud Hosting)
**NOTE:** ADSM was developed with the intention to move it towards a Cloud Hosted environment. It is setup to run as a webserver already. HOWEVER, it is not multi-user friendly yet so should not be setup in this way except for demo purposes.

Installing on a Server does not required a compiled frontend, only a compiled CEngine. These steps will be similar to setting up a development environment in that the Server will serve the program directly from a Python Virtual Environment.

1. Instructions not yet ready...

## Updating ADSM As An End User
ADSM has a bundled update program which can handle updating and fixing corrupted installations of the program.  
This update process works in both Production and Beta releases.

### Updating From Within ADSM
You can update ADSM from within the Frontend GUI.

1. Launch the application.
1. Open the "Settings Panel" with the cog button on the right.
1. Your current version will be listed as  
   "You are running...  
   x.x.x.x"
1. Below your current version, one of the following messages will be visible:
   1. "No updates are available."
   1. "A newer version of ADSM is available.  
   x.x.x.x"
   1. "A newer version of ADSM is available.  
   Integrity Error!"
   1. "A newer version of ADSM is available.  
   New Update Client"
1. If there are no updates, no button will appear.
1. If there is a newer version or there us a new Update Client, a button will appear that says "update ADSM".
   1. Pushing this button will launch the Update Client in a new Terminal Window and automatically close down ADSM.
   1. This Terminal Window may have prompts which you need to answer by typing 'y' or 'n' and pressing Enter.
   1. If your User does not have write access to the folder ADSM is installed in, the Update Client may fail. At this point, you will need to follow the instructions for Updating Manually.
1. If there is an Integirty Error, a button will appear that says "repair installation".
   1. An Integrity Error may occur if the Update Client detects any of the files that are part of the ADSM program are missing or corrupt.  
      **NOTE:** The Update Client cannot recover from a missing or corrupt ADSM or NPU executable.
   1. Pushing this button will launch the Update Client in a new Terminal Window and automatically close down ADSM.
   1. This Terminal Window may have prompts which you need to answer by typing 'y' or 'n' and pressing Enter.
   1. If your User does not have write access to the folder ADSM is installed in, the Update Client may fail. At this point, you will need to follow the instructions for Updating Manually.

### Updating Manually (if Administrator Rights required)
You can run the Update Client manually outside of the ADSM application.  
This can be useful if you need to run the update process with elevated rights as an Admin.

1. Run 'npu.exe' or 'npu' in the ADSM installation folder.
   1. On Windows, Right-Click and "Run As Administrator" if required.
   1. On Linux, use 'sudo' or run as the root user if required.
1. The Update Client will either launch in a new Terminal Window or run in the active terminal.
1. This Terminal Window may have prompts which you need to answer by typing 'y' or 'n' and pressing Enter.

## ADSM Project Code Overview
There are two main applications to the ADSM project and three support applications provided by Newline Technical Innovations.

**ADSM-CEngine** ( https://github.com/NAVADMC/ADSM-CEngine ) is the C code that runs the stochastic modeling simulation.  
Scenario parameters are sent to the CEngine via a Scenario SQLite file.  
Results are written back via stdout, and supplemental result files are written to a directory alongside the SQLite scenario file.

**ADSM** ( https://github.com/NAVADMC/ADSM ) is the main Frontend GUI that users will be interacting with. It creates scenarios by storing their parameters in a SQLite file and displays results after running a simulation.  
A more detailed breakdown of this application will follow.

**Django-ProductionServer** ( https://github.com/BryanHurst/django-productionserver ) is a cross-platform local application server utilizing CherryPy and Nginx for hosting Django projects locally on a desktop environment. 

**Viewer** is a distribution of Chromium customized by Newline Technical Innovations for displaying web based applications hosted locally.

**NPU**, or Newline Program Updater, is an application created by Newline Technical Innovations with an endpoint server hosted by Newline for getting updates to the installed ADSM application. NPU will also detect and attempt to repair a bad/corrupt installation.

### ADSM Breakdown
The ADSM Frontend Application is written in Python and utilizes a modified copy of the Django Web Framework.

You will want to read up on the [Django docs](https://docs.djangoproject.com/en/1.6/) and their very useful [tutorial](https://docs.djangoproject.com/en/1.6/intro/tutorial01/). 

As it is a Python project, the ADSM Frontend does NOT need to be compiled for testing or deployment on a web server.  
The compile process for the Frontend application is solely to create a distributable that can be installed and run standalone on an End User's system.  
Windows is currently the primary target of distribution compilation.  
However, you can run the ADSM Frontend on any system by setting up a Python Virtual Environment as will be detailed below in "Installing ADSM For Development".

The following is a short description of the Django "apps" of the ADSM Frontend Application.

#### ADSM
The base app which holds the settings and site wide static files.

There are a few things to note about the settings of this project.

1. The 'settings' file will attempt to detect where to create the workspace directory.
   1. It first looks to see if there is a user defined workspace in a 'settings.ini' file.
   1. If not, it will take the path as defined in either 'development_settings' or 'production_settings' (depending on which is used).
   1. If still not defined, it will find the User's Home directory and place the workspace there.
1. There are 'development_settings' and a reference 'production_settings'.
   1. Development settings are used when in development and when in a desktop deploy environment (compiled frontend).
   1. Production settings are referenced for future use in deploying to a web server.
1. A DB directory is placed under the Workspace directory.
1. Two databases are defined: default and scenario_db.
   1. Default is for the 'ADSMSettings' application and scenario independent stats tracking.
   1. Scenario is for everything to be stored in active_session or in a scenario database.
   
#### ADSMSettings
Application used to store user settings and track simulation progress. This is mostly behind the scenes data storage.

#### Database Templates
These are the blank state databases for a scenario (blanks.db) and the ADSMSettings app (settings.db).  
Blank state databases are required to help the program startup faster so the database doesn't have to be created from the schema each time.
 
#### Results
The application which runs simulations and parses results returned from the CEngine.  
The parsed results are written to the scenario db under the Results app and allows for displaying results graphically.

#### Sample Scenarios
Where sample scenarios and populations are stored for distribution with the application.

#### ScenarioCreator
The main portion of the ADSM Frontend.  
This is where the user will spend most of their time creating a scenario and inputting parameters. 

#### Viewer
As described above.

#### bin
This folder is where the ADSM-CEngine and its dependencies will be placed. The results app looks here for the simulation executable. 

#### build
This folder is not part of the repo, but will be generated when you compile the Frontend for distribution.

#### development_scripts
Some useful scripts used during development either for discovery, testing, or benchmarking.  
These are not used in the program at all.

#### dist
This folder is not part of the repo, but will be generated when you create the installer for the compiled Frontend.

#### node_modules
This folder is not part of the repo, but will be created when setting up a development environment.  
This is where node packages specific to the ADSM project will be installed.

#### static
This folder is not part of the repo, but may be generated when doing production testing.

## Installing ADSM For Development
When you install ADSM for Development, you can run the Frontend locally without the need for compiling. This is useful for testing and web hosting.

**Supported Operating Systems:**
- x86-64 Windows (automated compile)
- x86-64 Debian based Linux Systems (Ubuntu preferred) (manual intervention compile)

### x86-64 Windows 7 - 10
1. Install Python 3.4.2 x64 from: https://www.python.org/ftp/python/3.4.2/python-3.4.2.amd64.msi
1. Install Git from: https://git-scm.com/download/win  
   **NOTE:** Make sure you put it on your path so it can be used from the Windows Command Prompt. Also have it checkout line endings as-is and commit Unix style line endings.
1. Install Visual Studio 2010 from: http://download.microsoft.com/download/D/B/C/DBC11267-9597-46FF-8377-E194A73970D6/vs_proweb.exe  
   **NOTE:** Installing the trial is fine as all we need is the compiler. Where VS the GUI App may stop working after 30 days, the CLI compiler should continue to be valid.
1. In your favorite text editor, modify 'DRIVE:\\\\path\\to\\python34\\Lib\\distutils\\msvc9compiler.py':
   - After `ld_args.append('/MANIFESTFILE:' + temp_manifest)` add `ld_args.append('/MANIFEST')` at the same indentation level.
1. Install Mercurial from: https://www.mercurial-scm.org/release/windows/mercurial-4.1.3-x64.msi  
   **NOTE:** Make sure you put it on your system path so it can be used from the Windows Command Prompt.
1. Install Node LTS x64 from: https://nodejs.org/dist/v6.9.1/node-v6.9.1-x64.msi
1. Install Nullsoft Scriptable Install system (version shouldn't matter) from: http://nsis.sourceforge.net/Download
1. Open a Command Window in the directory you keep your projects (DRIVE:\\\\path\\to\\projects).
1. `DRIVE:\\path\to\python34\python -m venv DRIVE:\\path\to\projects\adsm_venv`
1. `DRIVE:\\path\to\projects\adsm_venv\Scripts\activate.bat`
1. Ensure that both `python` and `pip` commands are located in the virtual environment created above by doing `where python` and `where pip`.
   - If activation did not work and the two commands are using your system level commands, replace all calls below to python and/or pip with `DRIVE:\\path\to\projects\adsm_venv\Scripts\python.exe` or `DRIVE:\\path\to\projects\adsm_venv\Scripts\pip.exe` 
1. `cd DRIVE:\\path\to\projects`
1. `git clone git@github.com:NAVADMC/ADSM.git`
1. `cd adsm`
1. `pip install -r Requirements.txt`
1. `pip install -r Requirements-Windows.txt`
1. Download all the Wheel (*.whl) files here: https://newline.us/ADSM/setup/
1. Install all the Whell files with `pip install DRIVE:\\path\to\downloads\wheelname`
1. `npm install`
1. Download PyWin32 from: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win-amd64-py3.4.exe/download
1. `DRIVE:\\path\to\projects\adsm_venv\Scripts\easy_install.exe DRIVE:\\path\to\downloads\pywin32-219.win-amd64-py3.4.exe`
1. `pip install hg+https://bitbucket.org/BryanHurst/cx_freeze`  
   **WARNING:** This may not work! If not, follow these instructions:
   1. `pip install cx_freeze==4.3.4`
   1. In your favorite text editor, modify 'DRIVE:\\path\to\projects\adsm_venv\Lib\site_packages\cx_Freeze\finder.py':
      - Make the changes outline in this patch: https://bitbucket.org/BryanHurst/cx_freeze/commits/eba6cb644d390f69f07adbf9fdcead71ec0feebf?at=default
1. To run Selenium Tests:
   1. Download Chrome Driver from: http://chromedriver.storage.googleapis.com/2.12/chromedriver_win32.zip
   1. Unzip the file and place it in the Scripts folder of your new Virtual Environment (DRIVE:\\\\path\\to\\projects\\adsm_venv\\Scripts\\)
   
### x86-64 Debian Linux (Ubuntu preferred)
**WARNING:** You cannot use the Python which is shipped with the OS or that is installed via aptitude due to broken links to requirements that cx_freeze will need for compiling a distributable.

1. Requires ldd and objdump installed (probably already on your system)
1. `sudo su` (or be logged in as root)
1. `apt-get install git mercurial build-essential python3-dev`
1. `apt-get build-dep python3-matplotlib python3-scipy`
1. `curl -sL https://deb.nodesource.com/setup_4.x | bash -`
1. `apt-get install -y nodejs`
1. Python 3 ships with a broken pip, so fix it with: `curl https://bootstrap.pypa.io/get-pip.py | python3`
1. Custom compile Python 3 to fix broken dependency links:
   1. `apt-get install zlib1g-dev libbz2-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev libgdbm-dev liblzma-dev tk8.5-dev`
   1. `exit` (to exit sudo if you want to build ADSM as a lesser User)
   1. `cd`
   1. `wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz`
   1. `tar zxvf Python-3.4.3.tgz`
   1. `rm Python-3.4.3.tgz`
   1. `cd Python-3.4.3/`
   1. `./configure --prefix=/path/to/projects/adsm_python --exec_prefix=/path/to/projects/adsm_python`
   1. `make`
   1. `make altinstall`
   1. `cd ..`
   1. `rm -r Python-3.4.3`
   1. `/path/to/projects/adsm_python/bin/pip uninstall setuptools`
   1. `/path/to/projects/adsm_python/bin/pip uninstall pip`
   1. `wget https://pypi.python.org/packages/source/s/setuptools/setuptools-3.4.4.tar.gz`
   1. `tar -vzxf setuptools-3.4.4.tar.gz`
   1. `rm setuptools-3.4.4.tar.gz`
   1. `cd setuptools-3.4.4`
   1. `/path/to/projects/adsm_python/bin/python setup.py install`
   1. `cd ..`
   1. `rm -r setuptools-3.4.4/`
   1. `wget https://pypi.python.org/packages/source/p/pip/pip-1.5.6.tar.gz`
   1. `tar -vzxf pip-1.5.6.tar.gz`
   1. `rm pip-1.5.6.tar.gz`
   1. `cd pip-1.5.6`
   1. `/path/to/projects/adsm_python/bin/python setup.py install`
   1. `cd ..`
   1. `rm -r pip-1.5.6`
1. `cd /path/to/projects`
1. `git clone git@github.com:NAVADMC/ADSM.git`
1. `cd adsm`
1. `/path/to/projects/adsm_python/bin/pip install -r Requirements.txt`
1. `/path/to/projects/adsm_python/bin/pip install -r Requirements-Nix.txt`
1. `/path/to/projects/adsm_python/bin/pip install hg+https://bitbucket.org/BryanHurst/cx_freeze`  
   **WARNING:** This may not work! If not, follow these instructions:
   1. `cd /path/to/projects`
   1. `hg clone hg+https://bitbucket.org/BryanHurst/cx_freeze`
   1. `cd cx_freeze`
   1. `/path/to/projects/adsm_python/bin/python setup.py install`
   1. `cd ..`
   1. `rm -r cx_freeze`
   1. `cd /path/to/projects/adsm`
1. `npm install`
1. To run Selenium Tests:
   1. Download Chrome Driver from: http://chromedriver.storage.googleapis.com/2.12/chromedriver_linux64.zip
   1. Unzip the file and place it in the bin folder of your adsm_python.
   
### Run ADSM
During Development, it would be a pain to continually build the project just for testing.  
Thankfully, this is a Python project and so does not actually need to be compiled to run if you have the Virtual Environment setup.

Just like if you were to install ADSM on a server for hosting cloud services, you don't need a compiled distributable.

#### Windows
`DRIVE:\\path\to\projects\adsm_venv\Scripts\python.exe DRIVE:\\path\to\projects\adsm\manage.py devserver`

#### Linux
`/path/to/projects/adsm_python/bin/python /path/to/projects/adsm/manage.py devserver`

## Development and Production Branches
List of Relevant Branches: master, Stable

Development should be done in feature branches and merged into master. Master is the general development branch, and where Beta releases come from.  
**Master branch is what will be tagged in GitHub Pre-Release (Beta) Releases.**

Stable is the branch we merge master into when we are ready to do a production release.  
**Stable branch is what will be tagged in the GitHub Releases.** 

## Updating the Distributable
### Version Guide:
The version number is broken into four parts by periods: SimulationMajor.SimulationMinor.UIRelease.UIMinor/Beta.

1. Simulation Major Version is only ever changed when there is a fundamental difference in what the simulation is modeling.
1. Simulation Minor Version changes when there is a new feature available in the simulation, such as Vaccination Triggers, Vaccination Rings, or Within Unit Prevalence.
1. UI Release Version changes when there is an update to the UI, offering easier user interaction that is still compatible with older simulation files without any change. Each Release Version has a download available on the GitHub Release page.
1. UI Minor/Beta Version is the last digit and offers minor updates as the development process continues to fix UI quirks, release bug fixes or change UI layout.

Note that this does mean that the first two digits can advance without resetting the last two digits.  
A progression could be 3.3.4.5 -> 3.4.4.5.

The Master/Beta Branch will always be the first into a new UIRelease version.  
After pushing a Stable release, the next set of new feature work will bump the UIRelease version and reset the UIMinor version in the master branch (3.3.4.5 -> 3.3.5.0).  
Once work in master is deemed ready for release, Stable is bumped to the latest UIRelease.UIMinor version that we have been working on in master; meaning Stable won't see 3.3.5.1, 3.3.5.2... and so on but go directly to the current state of Master (3.3.5.8?).

### The NPU
The NPU server is currently hosted by Newline Technical Innovations. 

Developers will not need to log into the web panel provided by that server. 

Each release line of ADSM has a "Program_id" and "Password" associated with it on the NPU Server. You need the id and password to push release to the server. Please talk with your development team to acquire these sensitive credentials.

The ADSM releases are:

* ADSM (which is the Production release)
* ADSM_Beta
* ADSM_Vaccination_Rings

### When releaseing a Beta compile

1. The 'master' branch is setup specifically to compile Beta releases, so checkout master.
1. Bump the version in `ADSM/__init__.py` and in `package.json`
1. Build (with sourced python) `python setup.py build`
1. If this is work on a new set of features after a Stable release, then this is a new UIRelease and you need to make a GitHub release marked as "pre-release". The title of this release should be x.x.x.0, with the UIMinor always being a zero. Also create a beta tag on master. In the description, the ADSM version number should reflect the version in the title.
   - Windows/Linux: Create a zip file of your clean `build` directory and attach it to this new release.
1. If this is Minor work on a current UIRelease, then edit the GitHub release for the current UIRelease and update the ADSM Beta number in the description to the latest UIMinor number and create a new beta tag on master with this number. Do not update the release title, and do not update the attached zip file (people can pull changes via update).
1. Push the Update `cd build` `npu --create_update --program=ADSM_Beta --program_id=PROGRAM_ID --password=PASSWORD`
  
### When releasing a Production compile

1. The 'stable' branch is setup specifically to compile Production releases, so checkout Stable and merge master in when ready.
1. Bump the version in `ADSM/__init__.py`, in `package.json` and in `installer_windows.nsi`
1. Build (with sourced python) `python setup.py build`
1. If this is a new Stable release for a UIRelease version, then you need to make a new GitHub release. The title of this release should be x.x.x.0 matching exactly the title of the current Beta (minus "Beta"), with the UIMinor always being a zero. Also create a tab on Stable. In the description, the ADSM version number should reflect the latest version in master (x.x.x.x).
   - Windows: Run the nsi script and attach the output to the release.
   - Linux: Create a zip file of your clean `build` directory and attach it to this new release.
1. If this is a bug fix to a current release, then edit the GitHub release for the current UIRelease and update the ADSM version  number in the description to the latest UIMinor number and create a new tag on Stable with this number. Do not update the release title, and do not update the attached installer file (people can pull changes via update).
1. Push the Update `cd build` `npu --create_update --program=ADSM --program_id=PROGRAM_ID --password=PASSWORD` 

## Credits
Project Members:

* Project Owner - Missy Schoenbaum, USDA:APHIS:VS:CEAH Modeling Team contact melissa.schoenbaum@aphis.usda.gov
* ADSM Technical Lead - Josiah Seaman
* Simulation Creator / Maintainer - Neil Harvey
* Dev Ops - Bryan Hurst
* Project Management - Alex Pyle & Kurt Tometich, USDA Office of the CIO
* USDA Subject Matter Experts - Kelly Patyk, Amy Delgado, Columb Rigney, Kim Forde-Folle, Ann Seitzinger
* University of Minnesota Center for Food Protection Subject Matter Expert Tim Boyer
* Custom compiling Python libraries - Christoph Gohlke,  University of California, Irvine
* Student Externs: Conrad Selig, South Dakota School of Mines, Erin Campbell, University of Rochester
* R Collaborators: Karla Moreno-Torres, USDA ORISE Fellow, Matt Branan, USDA:APHIS:VS:CEAH

Noun Project Icons:

* "Spread" - Stephanie Wauters
