#ADSM (Animal Disease Spread Model)
An application with Desktop and Web Based GUI for creating a simulation model to assist decision making and education in evaluating animal disease incursions.  
This repo is the primary repo for the ADSM project and houses the main GUI that users will be interacting with.  
It creates scenarios by storing their parameters in a SQLite file and displays results after running a simulation.  
A more detailed breakdown of this application will follow.

##Installing ADSM As An End User
ADSM can be installed on either x86-64 Windows or x86-64 Debian based Linux Systems (Ubuntu preferred).  
This is a Beta and Release channel available for installation.

###Windows Release Channel
You can find the latest Release here: https://github.com/NAVADMC/ADSM/releases/latest

1. On the latest release page, download the "ADSM_Installer.exe".
1. Run the installer with admin privileges (ask your IT department for help if needed).
1. Follow the on screen prompts until Choose Install Location.
1. Choose the folder in which to install ADSM. This is where the program will reside. It is generally best to put it in "Program Files".
1. Choose the User Workspace folder for ADSM. If you are the only user of the computer, you can choose where to store your Workspace folder (folder of your scenarios). Note that you must have Read/Write access to the chosen folder. If ADSM is being installed on a shared computer and multiple users will use the program, leave this field BLANK so ADSM will find a suitable Workspace folder that is writable and unique to each user.
1. Continue following the on screen prompts.
1. When installation is complete, find "ADSM.exe" (either a shortcut on your desktop or in the folder you installed ADSM) and run it.
1. After launching the application, a black Terminal window with white text will appear. You can leave this window alone; some debug messages may appear in it.
1. A Viewer window will then appear on top of the Terminal window. This is where you will interface with the ADSM program.
1. To properly exit ADSM, close the Viewer window. Doing so will automatically close the Terminal window after saving and shutting down all processes.

###Debian Linux Release Channel
You can find the latest Release here: https://github.com/NAVADMC/ADSM/releases/latest

An installation process does not yet exist for Linux, so it is best for each user on a machine to download their own local copy of the program.

1. On the latest release page, download the "ADSM.tar.gz".
1. Extract the package into the folder in which you want ADSM to be installed. It is best to do this somewhere in your User space.
1. Run the "ADSM" executable in the extracted folder.
1. After launching the application, a terminal will appear. You can leave this terminal alone; some debug messages may appear in it.
1. A Viewer window will then appear on top of the terminal window. This is where you will interface with the ADSM program.
1. To properly exit ADSM, close the Viewer window. Doing so will automatically close the terminal after saving and shutting down all processes.

###Windows And Linux Beta Channel
You can find the latest Pre-release on the Releases page: https://github.com/NAVADMC/ADSM/releases

Beta builds do not come with an installer, so it is best for each user on a machine to download their own local copy of the program.

**WARNING:** If you have a Release installation on your computer, the Beta install MAY **overwrite your scenarios** from the Release version if you didn't specify a custom Workspace directory during Release install.   
If ADSM is selecting the Workspace directory automatically both the Release and Beta channel will select the same folder.

1. On the latest pre-release page, download either "ADSM_vx.x.x.x-beta_windows.zip" or "ADSM_vx.x.x.x-beta_linux.tar.gz"
1. Extract the package into the folder in which you want ADSM Beta to be installed. It is best to do this somewhere in your User space (a directory your user owns).
1. Run the "ADSM_Beta.exe" or "ADSM_Beta" executable in the extracted folder.
1. After launching the application, a terminal will appear. You can leave this terminal alone; runtime and debug messages will appear in it.
1. A Viewer window will then appear on top of the terminal window. This is where you will interface with the ADSM Beta program.
1. To properly exit ADSM Beta, close the Viewer window. Doing so will automatically close the terminal after saving and shutting down all processes.

###Installing ADSM On A Server (Cloud Hosting)
**NOTE:** ADSM was developed with the intention to move it towards a Cloud Hosted environment. It is setup to run as a webserver already. HOWEVER, it is not multi-user friendly yet so should not be setup in this way except for demo purposes.

1. Instructions to come...

##ADSM Project Code Overview
There are two main applications to the ADSM project and three support applications provided by Newline Technical Innovations.

**ADSM-CEngine** ( https://github.com/NAVADMC/ADSM-CEngine ) is the C code that runs the stochastic modeling simulation.  
Scenario parameters are sent to the CEngine via a Scenario SQLite file.  
Results are written directly back to the same SQLite file, and supplemental result files are written to a directory alongside the SQLite scenario file.

**ADSM** ( https://github.com/NAVADMC/ADSM ) is the main GUI that users will be interacting with. It creates scenarios by storing their parameters in a SQLite file and displays results after running a simulation.  
A more detailed breakdown of this application will follow.

**Django-ProductionServer** ( https://github.com/BryanHurst/django-productionserver ) is a cross-platform local application server utilizing CherryPy and Nginx for hosting Django projects locally on a desktop environment. 

**Viewer** is a distribution of Chromium customized by Newline Technical Innovations for displaying web based applications hosted locally.

**NPU**, or Newline Program Updater, is an application created by Newline Technical Innovations with an endpoint server hosted by Newline for getting updates to the installed ADSM application. NPU will also detect and attempt to repair a bad/corrupt installation.

###ADSM Breakdown
The ADSM GUI Application is written in Python and utilizes a modified copy of the Django Web Framework.

##Installing ADSM For Development

##Credits
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