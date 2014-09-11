from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from django.test import TestCase
from django.db import connections
import unittest

from Results.views import Simulation, simulation_process
from Results.models import DailyReport


class SimulationTest(TestCase):
    multi_db = True

    def test_multiple_threads(self):
        self.client.get('/app/OpenScenario/Roundtrip.sqlite3/')
        connections['default'].close()

        sim = Simulation(5)
        sim.start()
        sim.join()

        # 9 days for each iteration, so 45 reports total?
        self.assertEqual(DailyReport.objects.count(), 45)

    def test_single_thread(self):
        self.client.get('/app/OpenScenario/Roundtrip.sqlite3/')
        connections['default'].close()

        sim = Simulation(1)
        sim.start()
        sim.join()

        self.assertEqual(DailyReport.objects.count(), 9)
