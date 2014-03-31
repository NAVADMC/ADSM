from django.db import models
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session

class SmSession(Session):
    scenario_filename = models.CharField(max_length=255, default='', blank=True)
