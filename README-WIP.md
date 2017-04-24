# ADSM (Animal Disease Spread Model)
A Frontend application with Desktop and Web Based GUI for creating a simulation model to assist decision making and education in evaluating animal disease incursions.  
This repo is the primary repo for the ADSM project and houses the main Frontend that users will be interacting with.  
It creates scenarios by storing their parameters in a SQLite file and displays results after running a simulation.  
A more detailed breakdown of this application will follow.

## Installing ADSM As An End User
ADSM can be installed on either x86-64 Windows or x86-64 Debian based Linux Systems (Ubuntu preferred).  
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
Results are written directly back to the same SQLite file, and supplemental result files are written to a directory alongside the SQLite scenario file.

**ADSM** ( https://github.com/NAVADMC/ADSM ) is the main Frontend GUI that users will be interacting with. It creates scenarios by storing their parameters in a SQLite file and displays results after running a simulation.  
A more detailed breakdown of this application will follow.

**Django-ProductionServer** ( https://github.com/BryanHurst/django-productionserver ) is a cross-platform local application server utilizing CherryPy and Nginx for hosting Django projects locally on a desktop environment. 

**Viewer** is a distribution of Chromium customized by Newline Technical Innovations for displaying web based applications hosted locally.

**NPU**, or Newline Program Updater, is an application created by Newline Technical Innovations with an endpoint server hosted by Newline for getting updates to the installed ADSM application. NPU will also detect and attempt to repair a bad/corrupt installation.

### ADSM Breakdown
The ADSM Frontend Application is written in Python and utilizes a modified copy of the Django Web Framework.

## Installing ADSM For Development

## Credits
Project Members:

* Project Owner - Missy Schoenbaum, USDA:APHIS:VS:CEAH Modeling Team
* ADSM Technical Lead - Josiah Seaman
* Simulation Creator / Maintainer - Neil Harvey
* Dev Ops - Bryan Hurst
* Project Management - Alex Pyle & Kurt Tometich, USDA Office of the CIO
* USDA Subject Matter Experts - Kelly Patyk, Amy Delgado, Columb Rigney, Kim Forde-Folle, Ann Seitzinger
* University of Minnesota Center for Food Protection Subject Matter Expert Tim Boyer
* Custom compiling Python libraries - Christoph Gohlke,  University of California, Irvine

Noun Project Icons:

- "Spread" - Stephanie Wauters