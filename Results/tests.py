from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from django.test import TestCase

from ScenarioCreator.models import OutputSettings, ProductionType
from Results.models import DailyControls, DailyByProductionType, DailyByZone
from Results.summary import iteration_progress


class IterationProgressTestClass(TestCase):
    multi_db = True
    
    def setUp(self):
        self.settings, created = OutputSettings.objects.get_or_create(iterations=10)

    def test_no_iterations_started(self):
        self.assertEqual(iteration_progress(), 0)

    def test_no_iterations_completed(self):
        for i in range(10):
            for d in range(7):
                DailyControls.objects.create(iteration=i, day=d)
        self.assertEqual(iteration_progress(), 0.05)

    def test_two_iterations_completed_disease_end(self):
        self.settings.stop_criteria = "disease-end"
        self.settings.save()
        for i in range(10):
            for d in range(7):
                DailyControls.objects.create(iteration=i, day=d)
            if i < 8:
                DailyControls.objects.create(iteration=i, day=8, diseaseDuration=8)
        self.assertEqual(iteration_progress(), 0.8)

    def test_two_iterations_completed_first_detection(self):
        self.settings.stop_criteria = "first-detection"
        self.settings.save()
        cows, created = ProductionType.objects.get_or_create(name="cow")
        pigs, created = ProductionType.objects.get_or_create(name="pig")
        cats, created = ProductionType.objects.get_or_create(name="cat")
        for i in range(10):
            for d in range(7):
                DailyControls.objects.create(iteration=i, day=d)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=cows)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=pigs)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=cats)
            if i < 6:
                DailyControls.objects.create(iteration=i, day=8, diseaseDuration=8)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=cows, firstDetection=1)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=pigs, firstDetection=1)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=cats)
        self.assertEqual(iteration_progress(), 0.6)

    def test_two_iterations_completed_outbreak_end(self):
        self.settings.stop_criteria = "outbreak-end"
        self.settings.save()
        for i in range(10):
            for d in range(7):
                DailyControls.objects.create(iteration=i, day=d)
            if i < 4:
                DailyControls.objects.create(iteration=i, day=8, outbreakDuration=8)
        self.assertEqual(iteration_progress(), 0.4)

    def test_two_iterations_completed_stop_days(self):
        self.settings.stop_criteria = "stop-days"
        self.settings.days = 8
        self.settings.save()
        for i in range(10):
            for d in range(7):
                DailyControls.objects.create(iteration=i, day=d)
            if i < 2:
                DailyControls.objects.create(iteration=i, day=8)
        self.assertEqual(iteration_progress(), 0.2)