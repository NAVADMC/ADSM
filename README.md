SpreadModel has several external dependencies.  We recommend using pip to install them.
https://pypi.python.org/pypi/pip#downloads

Please note that SpreadModel is built against Python 3.3 which is incompatible with Python 2.x.

pip install django==1.6
pip install django-floppyforms==1.1
pip install django-crispy-forms
pip install django-extras
pip install django-debug-toolbar
pip install south
pip install selenium  # only necessary for testing
pip install cherrypy # local host server
pip install cx-freeze  # only necessary for creating executables

git clone https://github.com/NAVADMC/SpreadModel.git
git submodule init
git submodule update


SpreadModel uses to databases specified in ScenarioCreator/router.py.   Settings.sqlite3 is the "default" database that will be synced with all the stuff we don't want to change.  It doesn't have south migration tables at the moment.  The --database=scenario_db points to the file activeSession.sqlite3 and is declared in SpreadModel/settings.py and contains the apps "ScenarioCreator", "Results", and "south" which we want to change and reload every time we open a scenario.  If you rune syncdb it will say you need to run migrate for the other apps.  This command specifies the migration is directed at the non-default database.
    python manage.py migrate --database=scenario_db

Migrations are created using:
    python manage.py schemamigration ScenarioCreator --auto


Google Server Production Deploy:
sudo su
screen -r   (Ctrl+C to stop server) or (Ctrl+A  K   to kill the screen)
source /home/anaconda/bin/activate py3k
# make sure you have the production_server submodule
    git submodule init
    git submodule update
python manage.py runproductionserver --serve_static=collect --pid_file=server.pid --port=80