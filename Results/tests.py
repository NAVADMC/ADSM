from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from django.test import TransactionTestCase
import unittest

from Results.views import Simulation, simulation_process

class SimulationTest(TransactionTestCase):
    multi_db = True

    @unittest.skip("test cannot work due to it always testing the activeSession.sqlite3 db")
    def test_multiple_threads(self):
        self.client.get('')
        sim = Simulation(20)
        sim.start()

    @unittest.skip("test cannot work due to it always testing the activeSession.sqlite3 db")
    def test_single_thread(self):
        results = simulation_process(1)
        print(results)
