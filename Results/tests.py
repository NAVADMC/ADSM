from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from django.test import TestCase
import unittest

from Results.views import Simulation, simulation_process


class SimulationTest(TestCase):
    multi_db = True

    def test_multiple_threads(self):
        self.client.get('/setup/OpenScenario/Roundtrip.sqlite3/')

        sim = Simulation(5)
        sim.start()
        sim.join()

    @unittest.skip("test cannot work due to changes in parameters to the process function")
    def test_single_thread(self):
        results = simulation_process(1)
        print(results)
