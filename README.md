![BSD](https://cocoapod-badges.herokuapp.com/l/CocoaLumberjack/badge.png) 

ADSM (Animal Disease Spread Model)
==========

Setting up ADSM on your Windows Desktop
----------

For detailed installation instructions see: [How to Install ADSM](https://github.com/NAVADMC/ADSM/wiki/How-to-Install-ADSM)

__Overview:__  

1. Download the latest ADSM zip file from the [Releases Page](https://github.com/NAVADMC/ADSM/releases).
2. Extract the downloaded zip folder to your Desktop.
3. Run (double click) adsm.exe inside your new Desktop folder.
4. ADSM will create a workspace in "/Documents/ADSM Workspace" to store your scenarios. 
5. Consult the [User Guide](https://github.com/NAVADMC/ADSM/wiki#user-guide) to get started.


Setting up ADSM for Development Work
---------
If you are not a software developer working on modifying ADSM you can ignore the rest of this Readme file.

ADSM has several external dependencies. Getting your environment setup with these dependencies for development work will be outlined in this document.

Operating system:  

  - Windows, Debian Linux or Mac OS X. 
  
Python 3.4.2 (x64): 
 
  - Windows: https://www.python.org/ftp/python/3.4.2/python-3.4.2.amd64.msi
  - Linux: https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz (Please find instructions for compiling on your platform. Note: Ubuntu now ships with python3. We will give instructions assuming this version.)
    - Note that Linux Python3 ships with broken pip and setup tools. Run this command to fix the issue `curl https://bootstrap.pypa.io/get-pip.py | python3`
  - Mac: https://www.python.org/ftp/python/3.4.2/python-3.4.2-macosx10.6.pkg

Once Python is installed, you will need to create a Virtual Environment for the ADSM Project.  
This is important, especially if you plan on compiling a distributable version, as we will package the Virtual Environment to send off with the deployable. So make sure that your Virtual Environment is dedicated to this project and clean of unneeded package installations.

Create Virtual Environment:

  - Windows: `/path/to/py3.4/python -m venv /path/to/adsm_venv`
    - Activate with `/path/to/adsm_venv/Scripts/activate.bat`
  - Linux: `python3 -m venv /path/to/adsm_venv`
    - Activate with `source /path/to/adsm_venv/bin/activate`
    - Install required python dev files: `sudo apt-get install build-essential python3-dev; sudo apt-get build-dep python3-matplotlib`
    
Please make sure that NO packages from your global install made it into your Virtual Environment. Use `pip freeze` to confirm nothing is installed.

Now that we have a Virtual Environment, we need to install all the Python Packages that ADSM uses.  
Using the pip in your new Virtual Environment (confirm Virtual Environment Activation with `where pip` or `which pip`), install the following packages.

    pip install CherryPy==3.6.0
    pip install git+https://github.com/BryanHurst/django.git@stable/1.8.2-patched  # Note, this currently throws permission errors but actually works. Fix in Pip dev version.
    pip install Jinja2==2.7.3
    pip install MarkupSafe==0.23
    pip install django-crispy-forms==1.4.0
    pip install django-extras==0.3
    pip install django-floppyforms==1.2.0
    pip install futures==2.2.0
    pip install pyparsing==2.0.3
    pip install python-dateutil==2.3
    pip install pytz==2014.10
    pip install selenium==2.44.0
    pip install six==1.8.0
    pip install git+https://github.com/BryanHurst/django-productionserver.git@v1.0.2r2  # Note, this currently throws permission errors but actually works. Fix in Pip dev version.


**If you are on Linux or Mac**, then you can install the following:

    pip install numpy==1.9.1
    pip install matplotlib==1.4.2
    pip install pandas==0.15.2
    pip install pyproj==1.9.4
    pip install psutil==2.2.0

**If you are on Windows**, these packages need a special installation: 

  - Download the following files for Windows from [PythonLibs](http://www.lfd.uci.edu/~gohlke/pythonlibs/).  The exact links vary so you will need to navigate
  there manually.  Put them into a directory that you can easily navigate to in a command prompt:
    - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/numpy-MKL-1.9.1.win-amd64-py3.4.exe
    - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/pandas-0.15.2.win-amd64-py3.4.exe
    - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/matplotlib-1.4.2.win-amd64-py3.4.exe
    - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/pyproj-1.9.4dev.win-amd64-py3.4.exe
    - http://www.lfd.uci.edu/~gohlke/pythonlibs/psutil-2.2.0-cp34-none-win_amd64.whl
  - Now, using the easy_install (for exe) or pip (for whl) in your new Virtual Environment (`/path/to/adsm_venv/Scripts/easy_install`), install the following packages:
        
        easy_install numpy-MKL-1.9.1.win-amd64-py3.4.exe  
        easy_install pandas-0.15.1.win-amd64-py3.4.exe  
        easy_install matplotlib-1.4.2.win-amd64-py3.4.exe  
        easy_install pyproj-1.9.4dev.win-amd64-py3.4.exe  
        pip install psutil-2.2.0-cp34-none-win_amd64.whl

###Setup Pycharm IDE
The main developers of ADSM developed in Pycharm 4, so here's the IDE specific instructions to get your dev server running from a fresh clone.
* Launch Pycharm > Checkout from VCS > GitHub > Paste "git@github.com:NAVADMC/ADSM.git" into source (SSH method).
* Open up File > Settings.  Search "Django".  Languages and Frameworks > Django > 
    * root = C:\Users\Josiah\Documents\ADSM\
    * settings = ADSM/settings.py
    * Apply
* Search "Project".  Project: ADSM > Interpreter = path to your virtual environment folder.  Apply
* Project: ADSM > Project Structure. Tag every 'templates' folder as Templates.
    * ADSMSettings/templtates
    * Results/templtates
    * ScenarioCreator/templtates 
* Apply. Exit Settings.  Edit Run Configurations
    * '+' new run configuration > Django server
    * Name it ADSM
    * both checkboxes checked for including in PYTHONPATH
    * no other settings required

###Compile chain (optional)
If you plan on compiling a distributable version of the project, then use the following instructions.

Linux:  
 
  - Requires ldd and objdump installed (probably already on your system)  
  - `pip install hg+https://bitbucket.org/BryanHurst/cx_freeze`
    - If the above install fails, then there is a problem with your python shared libraries, I have a clone of the cx_freeze repo with a temp fix
      - CD to a directory where you want to download it, then `git clone git@git.newline.us:BryanHurst/cx_freeze.git; cd cx_freeze; python setup.py install`
 
Mac:  
 
  - Install Xcode  
  - `pip install hg+https://bitbucket.org/BryanHurst/cx_freeze`
 
Windows:  

  - Download the following two files:
    - http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win-amd64-py3.4.exe/download  
    - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/cx_Freeze-4.3.3.win-amd64-py3.4.exe
  - Now, using the easy_install in your new Virtual Environment (/path/to/adsm_venv/Scripts/easy_install), install the packages:
        
        easy_install pywin32-219.win-amd64-py3.4.exe
        easy_install cx_Freeze-4.3.3.win-amd64-py3.4.exe  # TODO: NOTE: This is outdated and will be revisited later

###Selenium Tests
To run the Selenium Tests, you will need Chrome or Chromium installed on your system plus the ChromeDriver v2.12.

Windows:  

  - http://chromedriver.storage.googleapis.com/2.12/chromedriver_win32.zip
  
Linux:  

  - http://chromedriver.storage.googleapis.com/2.12/chromedriver_linux64.zip
  
Mac:  

  - http://chromedriver.storage.googleapis.com/2.12/chromedriver_mac32.zip

Unzip the file and place it in the Scripts folder of your new Virtual Environment (/path/to/adsm_venv/Scripts/)


Development and Production Branches
-----------
List of Relevant Branches: master, Stable, Hotfix, Windows-staging, Windows, Linux-staging, Linux, Mac-OSX-staging, Mac-OSX

Development should be done in feature branches and merged into master. Master is the general development branch.

Stable is the branch we merge master into when we are ready to do testing before deploying to the OS Specific branches.  
**This branch is what will be tagged in the GitHub Releases.**  
Hotfix is the branch we push fixes to that need to be immediately promoted to the OS Production Branches without merging in current development work in master.  
Any time you merge from master to Stable, **also merge from master into Hotfix**.

After merging master into Stable and testing, merge Stable into each OS Staging branch.   
**NEVER merge master into a staging branch.**  
Make OS specific changes in their staging branches.

Once you are happy that the compiled version in each OS Staging branch is ready to go, merge each OS Staging into the main OS branch.  
This is the Production Branch for each OS.   
Distributables all update off of this branch, so NEVER merge directly to it! Only ever merge from their Staging branch.

If you need to push a patch to the distributions, make the changes in Hotfix. Merge Hotfix into Stable and do the testing as above, then merge Stable into the Production Branches.   
Once this is done, **make sure to merge Hotfix back into master as well**.

**NEVER merge any OS or OS-staging branch back into master.**  
If you do accidentally merge an OS branch into master, use this command to reset the repo before you push:
`git reset --merge <SHA>` 
Where <SHA> is the SHA from the latest commit on GitHub before the erroneous merge happened. This will reset the state back to the SHA.

Updating the adsm_simulation Executable
----------
Please never merge master into a staging branch just to compile the adsm_simulation executable.
If you need a one off compile of the adsm_simulation.exe, setup your own temporary branch or other compile directory.

    cd ADSM
    git pull
    cd CEngine
    sh bootstrap
    ./configure --disable-debug
    make

`make` will will fail on a `dia: command not found` error when it gets to the ADSM/CEngine/doc/diagrams directory.  That’s OK: at this point, the executable is built, and you are done.

Notes on the Distributable
----------
The Chromium Window should never need to be recompiled but instructions are provided here.        
For the Chromium window, we are using the Chromium Embedded Framework. Adobe hosts and maintains a site, cefbuilds.com, which has the compile chain setup in as a project per OS platform. I pulled the 64bit projects for each OS from the 2062 Branch on that site. 

 - Note, the Windows version requires VS2013  
 - Note, the Linux version require mesa-common-dev, libglew-dev, libgtkglext1-dev  
 - Note, in Linux this file needs to be linked on dev and normal user machines too! The distributable should handle this. `sudo ln -s /lib/x86_64-linux-gnu/libudev.so.1.3.5 /usr/lib/libudev.so.0`  

From here, I modified the 'cefsimple' application to launch http://localhost:8000, changed the window names, and disabled right clicking.  
Then compiled that project as x64 Release and put the output in the Viewer folder for the OS Branch.

Git needed to be put into the deployable, so we got a portable version for each OS. 

 - Git for windows, just downloaded portable from msysgit git repo.  
 - Linux, downloaded git source from github/git/git and compiled in new directory. Requires build-essential, libssl-dev, libcurl4-openssl-dev  

Building the Distributable
-----------
Cx_freeze must be installed.  
Required Items for cx_freeze:  

 - http://sourceforge.net/projects/pywin32/  (For Windows only)  
 - ldd, objdump  (For Linux only)  
 - Xcode  (For OS X only)  

Build steps:  

 - Merge master into Stable.  
 - Test.  
 - Push.
 - Make fixes in Master and repeat above until everything works.
 - Merge Stable into each OS-staging branch.  
 - Make OS Specific changes.  
 - Test.  
 - Run compile.py with your Virtual Env's Python (you can probably kill the process when it starts zipping the output).  
 - Test Compiled (`ADSM.exe --test`).
 - `git add -u` Commit as "OS Staging Compile mm/dd/yyyy @ HH:MM".
 - Push.
 - Merge OS-staging into OS branch. Do not merge in the Staging compiled files (ADSM.exe, adsm_update.exe, and library.zip). Do not merge in CEF or CEngine files. 
 - Test.
 - Run compile.py with your Virtual Env's Python.
 - Test Compiled (`ADSM.exe --test`).
 - `git add -u` Commit as "OS Production Compile mm/dd/yyyy @ HH:MM".
 - Push.

When you push the OS branch, that compiled version is now live and will be pulled down by all clients.
  
