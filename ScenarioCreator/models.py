from django.db import models

# Create your models here.
class Scenario(models.Model):
    description = models.CharField(max_length=255, default='Scenario Description', null=True, blank=True)
    naadsm_version = models.CharField(max_length=255, default='3.2.19')
    language = models.CharField(max_length=255, default='en', choices=(('en', "English"),('es', "Espanol")))
    num_runs = models.IntegerField(default=10)
    num_days = models.IntegerField(default=40)
    scenario_name = models.CharField(max_length=255, default='sample')
