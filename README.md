ADSM (Animal Disease Spread Model)
==========
Setting up ADSM for Development Work
---------
ADSM has several external dependencies. Getting your environment setup with these dependencies for development work will be outlined in this document.

 Operating system:
 
  - Windows, Debian Linux or Mac OS X.
  
 Python 3.4.2 (x64): 
 
  - Windows: https://www.python.org/ftp/python/3.4.2/python-3.4.2.amd64.msi
  - Linux: https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz (Please find instructions for compiling on your platform)
  - Mac: https://www.python.org/ftp/python/3.4.2/python-3.4.2-macosx10.6.pkg

Once Python is installed, you will need to create a Virtual Environment for the ADSM Project.
This is important, especially if you plan on compiling a distributable version, as we will package the Virtual Environment to send off with the deployable. So make sure that your Virtual Environment is dedicated to this project and clean of unneeded package installations.

Create Virtual Environment: `/path/to/py3.4/python -m venv /path/to/adsm_venv`

Now that we have a Virtual Environment, we need to install all the Python Packages that ADSM uses.
Using the pip in your new Virtual Environment (`/path/to/adsm_venv/Scripts/pip`), install the following packages.

    pip install CherryPy==3.6.0
    pip install Django==1.7.1
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


**If you are on Linux or Mac**, then you can install the following:

    pip install numpy==1.9.1

    # Linux requires a special step here: 
    sudo apt-get build-dep python-matplotlib

    pip install matplotlib==1.4.2
    pip install pandas==0.15.1
    pip install pyproj==1.9.4

**If you are on Windows**, these packages need a special installation. Download the following files for Windows into a directory that you can easily navigate to in a command prompt:

 - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/numpy-MKL-1.9.1.win-amd64-py3.4.exe
 - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/pandas-0.15.1.win-amd64-py3.4.exe
 - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/matplotlib-1.4.2.win-amd64-py3.4.exe
 - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/pyproj-1.9.4dev.win-amd64-py3.4.exe

Now, using the easy_install in your new Virtual Environment (`/path/to/adsm_venv/Scripts/easy_install`), install the following packages:

    easy_install numpy-MKL-1.9.1.win-amd64-py3.4.exe
    easy_install pandas-0.15.1.win-amd64-py3.4.exe
    easy_install matplotlib-1.4.2.win-amd64-py3.4.exe
    easy_install pyproj-1.9.4dev.win-amd64-py3.4.exe

###Compile chain (optional)
If you plan on compiling a distributable version of the project, then use the following instructions.

 Linux:  
  - Requires ldd and objdump installed (probably already on your system)  
  - `pip install cx-freeze==4.3.3`
 
 Mac:  
  - Install Xcode  
  - `pip install cx-freeze==4.3.3`
 
 Windows:  
 Download the following two files:  
 - http://sourceforge.net/projects/pywin32/files/pywin32/Build%20219/pywin32-219.win-amd64-py3.4.exe/download  
 - http://www.lfd.uci.edu/~gohlke/pythonlibs/2or7r828/cx_Freeze-4.3.3.win-amd64-py3.4.exe
 
 Now, using the easy_install in your new Virtual Environment (/path/to/adsm_venv/Scripts/easy_install), install the packages:  
    `easy_install pywin32-219.win-amd64-py3.4.exe`  
    `easy_install cx_Freeze-4.3.3.win-amd64-py3.4.exe`

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
List of Relevant Branches: master, Stable, Windows-staging, Windows, Linux-staging, Linux, Mac-OSX-staging, Mac-OSX

Development should be done in feature branches and merged into master. Master is the general development branch.

Stable is the branch we merge master into when we are ready to do testing before deploying to the OS Specific branches.  
**This branch is what will be tagged in the GitHub Releases.**

After merging master into Stable and testing, merge Stable into each OS Staging branch.   
**NEVER merge master into a staging branch.**  
Make OS specific changes in their staging branches.

Once you are happy that the compiled version in each OS Staging branch is ready to go, merge each OS Staging into the main OS branch.  
This is the Production Branch for each OS.   
Distributables all update off of this branch, so NEVER merge directly to it! Only ever merge from their Staging branch.

**NEVER merge any OS or OS-staging branch back into master.**  
If you do accidentally merge an OS branch into master, use this command to reset the repo before you push:
`git reset --merge <SHA>` 
Where <SHA> is the SHA from the latest commit on GitHub before the erroneous merge happened. This will reset the state back to the SHA.

Updating the adsm_simulation Executable
----------
Please never merge master into a staging branch just to compile the adsm_simulation executable.
If you need a one off compile of the adsm_simulation.exe, setup your own temporary branch or other compile directory.

    cd SpreadModel
    git pull
    cd CEngine
    sh bootstrap
    ./configure --disable-debug
    make

`make` will will fail on a `dia: command not found` error when it gets to the SpreadModel/CEngine/doc/diagrams directory.  That’s OK: at this point, the executable is built, and you are done.

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
 - Merge Stable into each OS-staging branch.  
 - Make OS Specific changes.  
 - Test.  
 - Compile.  
 - Test Compiled (`ADSM.exe --test`)  
 - Merge OS-staging into OS branch. Do not merge in the Staging compiled files (ADSM.exe, adsm_update.exe, and library.zip). Do not merge in CEF or CEngine files.  
 - Compile.  

When you push the OS branch, that compiled version is now live and will be pulled down by all clients.

