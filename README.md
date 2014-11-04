##Installing Animal Disease Spread Model (ADSM)
ADSM has several external dependencies.  We recommend using pip to install them.  We're currently using Python 2.7.8.
https://www.python.org/download
https://pypi.python.org/pypi/pip#downloads

    pip install django==1.6
    pip install django-floppyforms==1.2.0
    pip install django-crispy-forms
    pip install django-extras
    pip install south==0.8.4
    pip install future
    pip install futures  # This isn't a mistake, they're seriously two different packages. We're very futuristic here.
    pip install mpld3
    pip install jinja2
    pip install selenium  # only necessary for testing
    pip install cherrypy==3.5.0 --no-use-wheel # local host server

    pip install python-dateutil  
    pip install pyparsing  
    pip install pytz  
    #http://chromedriver.storage.googleapis.com/index.html?path=2.10/  places exe in your virtual_env/scripts folder

    git clone https://github.com/NAVADMC/SpreadModel.git
    git submodule init   # this fills out the 'production_server'
    git submodule update
    

### Matplotlib and Numpy Dependencies
For non-Windows machines:

    pip install numpy
    sudo apt-get build-dep python-matplotlib
    pip install matplotlib
    pip install pandas

For a new Python2.7 installation on Windows, you will need to download and install these binaries:  
http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy  
http://www.lfd.uci.edu/~gohlke/pythonlibs/#pandas  
http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib  


##Migrations
ADSM uses to databases specified in ScenarioCreator/router.py.   settings.sqlite3 is the "default" database that
will be synced with all the stuff we don't want to change.  It doesn't have south migration tables at the moment. 
The --database=scenario_db points to the file activeSession.sqlite3 and is declared in SpreadModel/settings.py and 
contains the apps "ScenarioCreator", "Results", and "south" which we want to change and reload every time we open a 
scenario.  If you rune syncdb it will say you need to run migrate for the other apps.  This command specifies the 
migration is directed at the non-default database.  It's critical to specify the database for apps otherwise it will
  say "no such table: south_migrationhistory".
```
python manage.py migrate --database=scenario_db
python manage.py migrate Results --database=scenario_db
python manage.py migrate ScenarioCreator --database=scenario_db
```

Migrations are created using:
`python manage.py schemamigration ScenarioCreator --auto`

###Initial Migrations
If you want to reset the migration history, this will break backwards compatibility with people's saved files.  You
will need to:
1) Make sure all your files are on the same migration.
2) Delete migration files (not the directory)
3) `python manage.py schemamigration Results --initial`
4) `python manage.py migrate Results --database=scenario_db --fake --delete-ghost-migrations`
5) I've also found creating a "New Scenario" works well:  http://127.0.0.1:8000/setup/NewScenario/

It's important that when you migrate you specify the database= because south does not use Django routers correctly.



##Google Server Production Deploy:
Ensure that you start server in a screen.  `screen -r` To avoid `sudo` Google server is forwarding port 80 to 8080.  You need
to be in the py33 virtual env.  That only needs to be done once.

    screen -r   (Ctrl+C to stop server and reuse the screen) or (Ctrl+A  K   to kill the screen and start from scratch)
    git pull
    git submodule update
    #source /home/josiah/py33/bin/activate 
    cd CEngine
    make
    cd ..
    python manage.py collectstatic
    python manage.py runproductionserver --serve_static=collect --pid_file=server.pid --port=8080 
    #sudo  iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080  # use this if the server crashes

##OS - specific Branches
_Branches: Windows, Linux, Mac-OSX_  
Never merge from OS specific branches back into master.  Changes made in these branches should be OS-specific and stay isolated.  Any general changes should be made in master and applied to the other branches by merging.  
If you do accidentally merge an OS branch into master use this command to reset the repo before you push:  
`git reset --merge <SHA>`  

Where <SHA> is the SHA from the latest commit on GitHub, before the erroneous merge happened.  This will reset the state back to the SHA.


##Bryan's Notes on Installing Python3.3 in Linux:
    sudo apt-get build-dep python3.2
    sudo apt-get install libreadline-dev libncurses5-dev libssl1.0.0 tk8.5-dev zlib1g-dev liblzma-dev
    wget http://python.org/ftp/python/3.3.3/Python-3.3.3.tgz
    tar xvfz Python-3.3.3.tgz
    cd Python-3.3.3
    ./configure --prefix=/opt/python3.3
    make
    sudo make install
    wget https://bootstrap.pypa.io/ez_setup.py -O - | sudo /opt/python3.3/bin/python3.3
    wget https://bootstrap.pypa.io/get-pip.py -O - | sudo /opt/python3.3/bin/python3.3

    ##For setting up the virtualenv for daily use:
        /opt/python3.3/bin/pyvenv ~/py33
        source ~/py33/bin/activate
        wget http://python-distribute.org/distribute_setup.py -O - | python
        easy_insatll pip

##Updating the ADSM Executable:
The production server already has the code checked out (Linux branch) and all
of the libraries required by ADSM are installed.

To update the executable:

    cd SpreadModel
    git pull
    cd CEngine
    sh bootstrap
    ./configure --disable-debug
    make

`make` will will fail on a `dia: command not found` error when it gets to the SpreadModel/CEngine/doc/diagrams directory.  That’s OK: at this point, the executable is built, and you are done.

##Building Distributable
    Required Items for cx_freeze:
        http://sourceforge.net/projects/pywin32/  # For Windows only. MAKE SURE these go into your virtualenv!
        ldd, objdump  # For Linux only
        Xcode  # For OS X only

    For the Chromium window, we are using the Chromium Embedded Framework. Compiling it is a massive pain,
    but thankfully Adobe hosts and maintains a site, cefbuilds.com, which has the compile chain setup in as a project per OS platform.

    I pulled the 64bit projects for each OS from the 2062 Branch on that site.
        Note, the Windows version requires VS2013
        Note, the Linux version require mesa-common-dev, libglew-dev, libgtkglext1-dev
            # NOTE: This file needs to be linked on normal user machines too!
            sudo ln -s /lib/x86_64-linux-gnu/libudev.so.1.3.5 /usr/lib/libudev.so.0

    From here, I modified the 'cefsimple' application to launch http://localhost:8000, changed the window names, and disabled right clicking.
    Compile that project as x64 Release and put the output in the Chromium folder for the OS Branch.

    The CEF Source was not added to the repo as it won't accept merges from the Google CEF Repo in the Project format made by Adobe.
    Also because this should really only be a one time thing to ever happen. However, the notes are here in case there is a major security hole that needs to be recompiled for.

    Git for windows, just downloaded portable from msysgit git repo.
    Linux, downloaded git source from github/git/git and compiled in new directory.
        requires build-essential, libssl-dev, libcurl4-openssl-dev

    GDAL. Required by Django. Usually Django uses a stubbed out library in its source.
    However, if the user has and GIS software installed, it messes up the path. So we need to specify a path to a library.
    Figured I would go ahead and use a real one instead of a stubbed one for possible future needs.
    www.gdal.org pointed to www.gisinternals.com where I downloaded the GDAL and MapServer Latest Release for Win64 (1600 GDAL).
    Got the binary only zip. From this pulled the gdal111.dll from the bin folder.
    This one file is enough to make django not complain. But I don't know if it is enough to actually do geo stuff later...
