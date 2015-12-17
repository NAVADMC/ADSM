![BSD](https://cocoapod-badges.herokuapp.com/l/CocoaLumberjack/badge.png) 

ADSM (Animal Disease Spread Model)
==========

Setting up ADSM on your Windows Desktop
----------

For detailed installation instructions see: [How to Install ADSM](https://github.com/NAVADMC/ADSM/wiki/How-to-Install-ADSM)

__Overview:__  

1. Download the latest ADSM zip file from the [Releases Page](https://github.com/NAVADMC/ADSM/releases).
2. Extract the downloaded zip folder to your Desktop or other desired location.
3. Run (double click) adsm.exe inside your new Desktop folder.
4. ADSM will create a workspace in "~/Documents/ADSM Workspace" to store your scenarios. 
5. Consult the [User Guide](https://github.com/NAVADMC/ADSM/wiki#user-guide) to get started.


Setting up ADSM for Development Work
---------
If you are not a software developer working on modifying ADSM you can ignore the rest of this Readme file.

ADSM has several external dependencies. Getting your environment setup with these dependencies for development work will be outlined in this document.

Operating system:  

  - Windows, Debian Linux, or Mac OS X (no Viewer application or packaged release). 
  
Python 3.4.2 (x64): 
 
  - Windows: https://www.python.org/ftp/python/3.4.2/python-3.4.2.amd64.msi
  - Linux: https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz (Please find instructions for compiling on your platform. Note: Ubuntu now ships with python3. We will give instructions assuming this version.)
    - Note that Linux Python3 ships with broken pip and setup tools. Run this command to fix the issue `curl https://bootstrap.pypa.io/get-pip.py | python3`
    - Note that if you plan to build a distributable for ADSM, you will need to compile your own python as documented below

Once Python is installed, you will need to create a Virtual Environment for the ADSM Project.  
This is important, especially if you plan on compiling a distributable version, as we will package the Virtual Environment to send off with the deployable. So make sure that your Virtual Environment is dedicated to this project and clean of unneeded package installations.

Create Virtual Environment:

  - Windows: `/path/to/py3.4/python -m venv /path/to/adsm_venv`
    - Activate with `/path/to/adsm_venv/Scripts/activate.bat`
    - Install Git and Mercurial so they are properly on the command line  #TODO: Get links for these
  - Linux: `python3 -m venv --without-pip /path/to/adsm_venv`  
    - Install Setuptools and Pip: `wget https://pypi.python.org/packages/source/s/setuptools/setuptools-3.4.4.tar.gz; tar -vzxf setuptools-3.4.4.tar.gz; rm setuptools-3.4.4.tar.gz; cd setuptools-3.4.4; python setup.py install; cd ..; rm -r setuptools-3.4.4; wget https://pypi.python.org/packages/source/p/pip/pip-1.5.6.tar.gz; tar -vzxf pip-1.5.6.tar.gz; rm pip-1.5.6.tar.gz; cd pip-1.5.6; python setup.py install; cd ..; rm -r pip-1.5.6`
    - Activate with `source /path/to/adsm_venv/bin/activate`
    - Install required dev files: `sudo apt-get install build-essential python3-dev git mercurial; sudo apt-get build-dep python3-matplotlib python3-scipy`
    
Please make sure that NO packages from your global install made it into your Virtual Environment. Use `pip freeze` to confirm nothing is installed.

Download the ADSM source: `git clone https://github.com/NAVADMC/ADSM.git /path/toADSM` (for read only) or `git clone git@github.com:NAVADMC/ADSM.git /path/to/ADSM` (for push access [must have dev access])

Now that we have a Virtual Environment, we need to install all the Python Packages that ADSM uses.  
Using the pip in your new Virtual Environment (confirm Virtual Environment Activation with `where pip` or `which pip`), install all the required packages in Requirements.txt `pip install -r Requirements.txt`

**If you are on Linux or Mac** install the extra packages: `pip install -r Requirements-Nix.txt`

**If you are on Windows** install the extra packages: `pip install -r Requirements-Windows.txt` 

  - Download the following files for Windows from [PythonLibs](http://www.lfd.uci.edu/~gohlke/pythonlibs/). Another possible location is [PNAWheels](https://nipy.bic.berkeley.edu/pna/wheels/)  The exact links vary so you will need to navigate
  there manually.  Put them into a directory that you can easily navigate to in a command prompt:
    - numpy-MKL-1.9.1.win-amd64-py3.4.exe
    - https://nipy.bic.berkeley.edu/pna/wheels/pandas-0.15.2-cp34-none-win_amd64.whl
    - matplotlib-1.4.2.win-amd64-py3.4.exe
    - pyproj-1.9.4dev.win-amd64-py3.4.exe
    - psutil-2.2.0-cp34-none-win_amd64.whl
    - https://nipy.bic.berkeley.edu/pna/wheels/scipy-0.15.1-cp34-none-win_amd64.whl
  - Now, using the easy_install (for exe) or pip (for whl) in your new Virtual Environment (`/path/to/adsm_venv/Scripts/easy_install` or `/path/toadsm_venv/Scripts/pip`), install the following packages:
        
        easy_install *.exe 
        pip install *.whl
        
###React Setup
Install Node (please x64 version)
cd BASE_DIR (Not an actual command. Go into the root of the project)
npm install

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
  - You need a custom compiled version of Python3.4 (will use instead of venv)
        
        sudo apt-get install zlib1g-dev libbz2-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev libgdbm-dev liblzma-dev tk8.5-dev
        wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
        tar zxvf Python-3.4.3.tgz
        rm Python-3.4.3.tgz
        cd Python-3.4.3/
        ./configure --prefix=/path/to/projects/adsm_python --exec_prefix=/path/to/projects/adsm_python
        make
        make altinstall
        /path/to/projects/adsm_python/bin/pip uninstall setuptools
        /path/to/projects/adsm_python/bin/pip uninstall pip
        wget https://pypi.python.org/packages/source/s/setuptools/setuptools-3.4.4.tar.gz
	    tar -vzxf setuptools-3.4.4.tar.gz
	    rm setuptools-3.4.4.tar.gz
	    cd setuptools-3.4.4
        /path/to/projects/adsm_python/bin/python setup.py install
        cd ..
        rm -r setuptools-3.4.4/
        wget https://pypi.python.org/packages/source/p/pip/pip-1.5.6.tar.gz
	    tar -vzxf pip-1.5.6.tar.gz
	    rm pip-1.5.6.tar.gz
	    cd pip-1.5.6
	    /path/to/projects/adsm_python/bin/python setup.py install
	    cd ..
	    rm -r pip-1.5.6
        
  - Using the new python, install all the requirements `/path/to/projects/adsm_python/bin/pip install -r /path/to/adsm/Requirements.txt && /path/to/projects/adsm_python/bin/pip install -r /path/to/adsm/Requirements-Nix.txt`     
  - `/path/to/projects/adsm_python/bin/pip install hg+https://bitbucket.org/BryanHurst/cx_freeze`
    - If the above install fails, then there is a problem with your python shared libraries, I have a clone of the cx_freeze repo with a temp fix
      - CD to a directory where you want to download it, then `git clone git@git.newline.us:BryanHurst/cx_freeze.git; cd cx_freeze; /path/to/projects/adsm_python/bin/python setup.py install`
  - If you need to update the NPU, `/path/to/projects/adsm_python/bin/pip install git+https://github.com/pyinstaller/pyinstaller.git@python3`
 
Windows:  

  - Download the following two files:
    - http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win-amd64-py3.4.exe/download  
    - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/cx_Freeze-4.3.3.win-amd64-py3.4.exe
  - Now, using the easy_install in your new Virtual Environment (/path/to/adsm_venv/Scripts/easy_install), install the packages:
        
        easy_install pywin32-219.win-amd64-py3.4.exe
        easy_install cx_Freeze-4.3.3.win-amd64-py3.4.exe  # TODO: NOTE: This is outdated and will be revisited later
        
  - Update cx_freeze:
    - Go to https://bitbucket.org/BryanHurst/cx_freeze/
    - Find all commits made after forking (generally commits made by Bryan) and note the files that have been changed
    - Copy these modified files into your installed cx_freeze folder in `/path/to/adsm_venv/Lib/site-packages/cx_Freeze-4.3.4-py3.4-win-amd64.egg/cx_Freeze

###Selenium Tests
To run the Selenium Tests, you will need Chrome or Chromium installed on your system plus the ChromeDriver v2.12.

Windows:  

  - http://chromedriver.storage.googleapis.com/2.12/chromedriver_win32.zip
  
Linux:  

  - http://chromedriver.storage.googleapis.com/2.12/chromedriver_linux64.zip

Unzip the file and place it in the Scripts or bin folder of your new Virtual Environment (/path/to/adsm_venv/Scripts/ || /path/to/adsm_vent/bin/)


Development and Production Branches
-----------
List of Relevant Branches: master, Stable

Development should be done in feature branches and merged into master. Master is the general development branch.

Stable is the branch we merge master into when we are ready to do a production release.  
**Stable branch is what will be tagged in the GitHub Releases.**    
Master is tagged in GitHub as pre-release.

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

Updating the Distributable
----------
When releaseing a Beta compile:

  - Bump the version in `ADSM/__init__.py` and in `package.json`
  - Build (with sourced python) `python setup.py build`
  - Push the Update `cd build` `npu.exe --create_update --program=ADSM_Beta --program_id=PROGRAM_ID --password=PASSWORD`
  - Update the latest pre-release with a new tag (don't change the release title)
  
When releasing a Production compile:

  - Bump the version in `ADSM/__init__.py`, in `package.json` and in `installer_windows.nsi`
  - Build (with sourced python) `python setup.py build`
  - Push the Update `cd build` `npu.exe --create_update --program=ADSM --program_id=PROGRAM_ID --password=PASSWORD` 
  - Update the latest release with a new tag (don't change the release title)
  - Run the nsi script and upload the output to the release
  
# Credits
* Project Owner - Missy Schoenbaum
* ADSM Technical Lead - Josiah Seaman
* Simulation Creator / Maintainer - Neil Harvey
* Dev Ops - Bryan Hurst
* Project Management - Alex Pyle & Kurt Tometich

## Noun Project icons:
* "Spread" - Stephanie Wauters