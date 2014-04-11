from django.db import models
from django.contrib.sessions.models import Session


class SmSession(models.Model):
    scenario_filename = models.CharField(max_length=255, default='', blank=True)
