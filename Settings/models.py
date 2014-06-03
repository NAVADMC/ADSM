from django.db import models
from django.contrib.sessions.models import Session


class SmSession(models.Model):
    scenario_filename = models.CharField(max_length=255, default='', blank=True)
    unsaved_changes = models.BooleanField(default=False)
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
