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

  - Windows (automated compile), Debian Linux (manual intervention compile), or Mac OS X (no Viewer application or packaged release). 
  
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
    - Install [Git](https://git-scm.com/download/win) so it is properly on the command line
    - install Visual Studio 2010: http://download.cnet.com/Microsoft-Visual-Studio-2010-Professional/3000-2212_4-10618634.html (Note: Installing the trial is fine as all we need is the compiler. Where VS the GUI App may stop working after 30 days, the CLI compiler should continue to be valid)
    - modify file `\path\to\py3.4\Lib\distutils\msvc9compiler.py` (Note: This is not in your venv, but your base python 3.4 install)
      - after `ld_args.append('/MANIFESTFILE:' + temp_manifest)` add `ld_args.append('/MANIFEST')` at the same indentation level
  - Linux: `python3 -m venv --without-pip /path/to/adsm_venv`  
    - Install Setuptools and Pip: `wget https://pypi.python.org/packages/source/s/setuptools/setuptools-3.4.4.tar.gz; tar -vzxf setuptools-3.4.4.tar.gz; rm setuptools-3.4.4.tar.gz; cd setuptools-3.4.4; python setup.py install; cd ..; rm -r setuptools-3.4.4; wget https://pypi.python.org/packages/source/p/pip/pip-1.5.6.tar.gz; tar -vzxf pip-1.5.6.tar.gz; rm pip-1.5.6.tar.gz; cd pip-1.5.6; python setup.py install; cd ..; rm -r pip-1.5.6`
    - Activate with `source /path/to/adsm_venv/bin/activate`
    - Install required dev files: `sudo apt-get install build-essential python3-dev git; sudo apt-get build-dep python3-matplotlib python3-scipy`
    
Please make sure that NO packages from your global install made it into your Virtual Environment. Use `pip freeze` to confirm nothing is installed.

Download the ADSM source: `git clone https://github.com/NAVADMC/ADSM.git /path/toADSM` (for read only) or `git clone git@github.com:NAVADMC/ADSM.git /path/to/ADSM` (for push access [must have dev access])

Now that we have a Virtual Environment, we need to install all the Python Packages that ADSM uses.  
Using the pip in your new Virtual Environment (confirm Virtual Environment Activation with `where pip` or `which pip`), install all the required packages in Requirements.txt `pip install -r Requirements.txt`

**If you are on Linux or Mac:** 

  - install the extra packages: `pip install -r Requirements-Nix.txt`

**If you are on Windows:** 

  - install the extra packages: `pip install -r Requirements-Windows.txt`
  - Download all the Wheel (*.whl) files located here: https://newline.us/ADSM/setup/
  - install numpy: `pip install numpy-1.9.3+mkl-cp34-none-win_amd64.whl`
  - install matplotlib: `pip install matplotlib-1.4.3-cp34-none-win_amd64.whl`
  - install pandas: `pip install pandas-0.15.2-cp34-none-win_amd64.whl`
  - install scipy: `pip install scipy-0.15.1-cp34-none-win_amd64.whl`
  - install pyproj: `pip install pyproj-1.9.4-cp34-none-win_amd64.whl`
  - install psutil: `pip install psutil-2.2.1-cp34-none-win_amd64.whl`
                
###React Setup
Install Node (please x64 version)
cd BASE_DIR (Not an actual command. Go into the root of the project)
npm install

###Compile chain (optional)
If you plan on compiling a distributable version of the project, then use the following instructions.

Linux:  
 
  - Requires ldd and objdump installed (probably already on your system)
  - Install Mercurial `sudo apt-get install mercurial`
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
      - CD to a directory where you want to download it, then `hg clone hg+https://bitbucket.org/BryanHurst/cx_freeze; cd cx_freeze; /path/to/projects/adsm_python/bin/python setup.py install`
  - If you need to update the NPU, `/path/to/projects/adsm_python/bin/pip install git+https://github.com/pyinstaller/pyinstaller.git@python3`
 
Windows:  

  - Install Mercurial so it is properly on your path
  - Download PyWin32 from: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win-amd64-py3.4.exe/download
  - Using the easy_install in your new Virtual Environment (/path/to/adsm_venv/Scripts/easy_install), install PyWin32:
        
        `easy_install pywin32-219.win-amd64-py3.4.exe`
        
  - Using /path/to/adsm_venv/Scripts/pip install cx_freeze:
  
        `pip install hg+https://bitbucket.org/BryanHurst/cx_freeze`

###Selenium Tests
To run the Selenium Tests, you will need Chrome or Chromium installed on your system plus the ChromeDriver v2.12.

Windows:  

  - http://chromedriver.storage.googleapis.com/2.12/chromedriver_win32.zip
  
Linux:  

  - http://chromedriver.storage.googleapis.com/2.12/chromedriver_linux64.zip

Mac:

  - http://chromedriver.storage.googleapis.com/2.12/chromedriver_mac32.zip

Unzip the file and place it in the Scripts or bin folder of your new Virtual Environment (/path/to/adsm_venv/Scripts/ || /path/to/adsm_vent/bin/)


Development and Production Branches
-----------
List of Relevant Branches: master, Stable

Development should be done in feature branches and merged into master. Master is the general development branch, and where Beta releases come from.

Stable is the branch we merge master into when we are ready to do a production release.  
**Stable branch is what will be tagged in the GitHub Releases.**    
Master is tagged in GitHub as pre-release.

Updating the adsm_simulation Executable
----------

    cd ADSM
    git pull
    cd CEngine
    sh bootstrap
    ./configure --disable-debug
    make

`make` will will fail on a `dia: command not found` error when it gets to the ADSM/CEngine/doc/diagrams directory.  That’s OK: at this point, the executable is built, and you are done.

Copy the executable into the `bin` folder and commit it after testing.

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
* Project Owner - Missy Schoenbaum, USDA:APHIS:VS:CEAH Modeling Team
* ADSM Technical Lead - Josiah Seaman
* Simulation Creator / Maintainer - Neil Harvey
* Dev Ops - Bryan Hurst
* Project Management - Alex Pyle & Kurt Tometich, USDA Office of the CIO
* USDA Subject Matter Experts - Kelly Patyk, Amy Delgado, Columb Rigney, Kim Forde-Folle, Ann Seitzinger
* University of Minnesota Center for Food Protection Subject Matter Expert Tim Boyer
* Custom compiling Python libraries - Christoph Gohlke,  University of California, Irvine

## Noun Project icons:
* "Spread" - Stephanie Wauters
