from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
import ScenarioCreator.views
from Settings.views import update_is_needed

standard_library.install_hooks()
from django.db import models, OperationalError
from django.contrib.sessions.models import Session


class SmSession(models.Model):
    scenario_filename = models.CharField(max_length=255, default="Untitled Scenario", blank=True)
    unsaved_changes = models.BooleanField(default=False)
    update_needed = models.BooleanField(default=False, help_text='Is there are new version of ADSM available?')
    population_upload_status = models.CharField(null=True, blank=True, max_length=255)
    population_upload_percent = models.FloatField(default=0)

    def set_population_upload_status(self, status=None, percent=None):
        if status:
            self.population_upload_status = status
        if percent:
            self.population_upload_percent = float(percent)
        self.save()

    def reset_population_upload_status(self):
        self.population_upload_status = None
        self.population_upload_percent = 0
        self.save()


def unsaved_changes(new_value=None):
    session = SmSession.objects.get_or_create(id=1)[0]  # This keeps track of the state for all views and is used by basic_context
    if new_value is not None:  # you can still set it to False
        session.unsaved_changes = new_value
        session.save()
    return session.unsaved_changes


def scenario_filename(new_value=None):
    session = SmSession.objects.get_or_create(id=1)[0]  # This keeps track of the state for all views and is used by basic_context
    if new_value:
        session.scenario_filename = new_value.replace('.sqlite3', '')
        session.save()
    return session.scenario_filename


def update_status(do_update=False):
    try:
        session = SmSession.objects.get_or_create(id=1)[0]
    except OperationalError:
        ScenarioCreator.views.reset_db('default')  # I'm doing this instead of graceful_startup() to avoid long migrations on startup
        return update_status(do_update)  # possible infinite loop
    if do_update:
        session.update_needed = update_is_needed()
        session.save()
    return session.update_needed

