##Installing Animal Disease Spread Model (ADSM)
ADSM has several external dependencies.  We recommend using pip to install them.
https://pypi.python.org/pypi/pip#downloads

Please note that ADSM is built against Python 3.3 which is incompatible with Python 2.x.  

    pip install django==1.6
    pip install django-floppyforms==1.1
    pip install django-crispy-forms
    pip install django-extras
    pip install django-debug-toolbar
    pip install south
    pip install selenium  # only necessary for testing
    pip install cherrypy # local host server
    pip install cx_freeze  # only necessary for creating executables https://pypi.python.org/pypi/cx_Freeze NOTE: Needed to edit C:\Python33\Scripts\cxfreeze and csfreeze-quickstart to point to correct interpreter!

    git clone https://github.com/NAVADMC/SpreadModel.git
    git submodule init   # this fills out the 'production_server'
    git submodule update

### Matplotlib and Numpy Dependencies
For a new Python3.3 installation on Windows, you will need to download these binaries:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
http://www.lfd.uci.edu/~gohlke/pythonlibs/#pandas
http://www.lfd.uci.edu/~gohlke/pythonlibs/#matplotlib
    pip install git+https://github.com/josiahseaman/django-extras
    pip install python-dateutil
    pip install pyparsing
    pip install pytz

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
    sudo su
    screen -r   (Ctrl+C to stop server and reuse the screen) or (Ctrl+A  K   to kill the screen and start from scratch)
    git pull
    git submodule update
    source /home/anaconda/bin/activate py3k    #only necessary once
    python manage.py collectstatic
    python manage.py runproductionserver --serve_static=collect --pid_file=server.pid --port=80

##OS - specific Branches
_Branches: Windows, Linux, Mac-OSX_  
Never merge from OS specific branches back into master.  Changes made in these branches should be OS-specific and stay isolated.  Any general changes should be made in master and applied to the other branches by merging.


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

