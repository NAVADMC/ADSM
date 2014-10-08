from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from django.test import TestCase
from django.db import connections
import unittest
import time
import os, shutil
import zipfile

from Results.views import Simulation, simulation_process
from Results.models import DailyReport
from ScenarioCreator.models import OutputSettings, ProductionType, Zone
from Results.models import DailyControls, DailyByProductionType, DailyByZone, DailyByZoneAndProductionType
from Results.summary import iteration_progress, summarize_results
from Results.output_parser import DailyParser
from Settings.models import scenario_filename
from Settings.utils import close_all_connections


class SimulationTest(TestCase):
    multi_db = True

    @classmethod
    def setUpClass(cls):
        source_db = os.path.join('workspace', 'Roundtrip.sqlite3')
        cls.destination_db = os.path.join('workspace', 'Roundtrip_test.sqlite3')
        shutil.copy(source_db, cls.destination_db)
        cls.scenario_directory = os.path.join('workspace', 'Roundtrip_test')

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.destination_db)

    def setUp(self):
        self.client.get('/app/OpenScenario/Roundtrip_test.sqlite3/')

        settings = OutputSettings.objects.first()
        settings.stop_criteria = 'stop-days'
        settings.days = 4
        settings.save()
        close_all_connections()

    def tearDown(self):
        shutil.rmtree(self.scenario_directory, ignore_errors=True)

    def test_multiple_threads(self):
        sim = Simulation(5)
        sim.start()
        sim.join()

        # 4 days for each iteration, so 20 reports total
        self.assertEqual(DailyReport.objects.count(), 20)

    def test_single_thread(self):
        sim = Simulation(1)
        sim.start()
        sim.join()

        self.assertEqual(DailyReport.objects.count(), 4)

    def test_supplemental_output_created(self):
        """
            Ensures that prepare_supplemental_output_directory
            is being called, and that the directory created is
            being passed to adsm properly
        """
        settings = OutputSettings.objects.first()
        settings.save_daily_unit_states = True
        settings.save()
        close_all_connections()
        output_file = os.path.join(self.scenario_directory, 'states_1.csv')

        sim = Simulation(1)
        sim.start()
        sim.join()

        self.assertTrue(os.access(output_file, os.F_OK))

    def test_map_zip_with_output(self):
        settings = OutputSettings.objects.first()
        settings.save_daily_unit_states = True
        settings.save_map_output = True
        settings.save()
        close_all_connections()
        file_name = os.path.join(self.scenario_directory, 'Roundtrip_test Map Output.zip')
        folder_name = os.path.join(self.scenario_directory, 'Map')

        sim = Simulation(1)
        sim.start()
        sim.join()

        self.assertTrue(os.access(file_name, os.F_OK))

        with zipfile.ZipFile(file_name, 'r') as zf:
            self.assertListEqual(zf.namelist(), os.listdir(folder_name))

    def test_map_zip_no_output(self):
        settings = OutputSettings.objects.first()
        settings.save_map_output = False
        settings.save()
        close_all_connections()
        file_name = os.path.join(self.scenario_directory, 'Roundtrip_test Map Output.zip')
        folder_name = os.path.join(self.scenario_directory, 'Map')

        sim = Simulation(1)
        sim.start()
        sim.join()

        self.assertTrue(os.access(file_name, os.F_OK))

        with zipfile.ZipFile(file_name, 'r') as zf:
            self.assertEqual(len(zf.namelist()), 0)
            self.assertListEqual(zf.namelist(), os.listdir(folder_name))


class IterationProgressTestClass(TestCase):
    multi_db = True
    
    def setUp(self):
        self.settings, created = OutputSettings.objects.get_or_create(iterations=10)

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


class ParserTests(TestCase):
    multi_db = True

    def test_initialize(self):
        cattle = ProductionType.objects.create(name="Cattle")
        medium_risk = Zone.objects.create(name="Medium Risk", radius=5.0)
        header_line = "Run,Day\r\n"

        p = DailyParser(header_line)

        self.assertEqual(p.headers, ['Run', 'Day'])
        self.assertEqual(p.possible_zones, {'Medium Risk', 'Background'})
        self.assertEqual(p.possible_pts, {'', 'Cattle'})

    def test_parse_single_field_in_controls(self):
        header_line = "Run,Day,outbreakDuration\r\n"
        p = DailyParser(header_line)

        adsm_iteration_output = ["1,1,1"]

        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], DailyControls)
        self.assertEqual(results[0].outbreakDuration, 1)

    def test_parse_single_field_in_daily_by_production_type(self):
        cows, created = ProductionType.objects.get_or_create(name="Cattle")
        header_line = "Run,Day,firstDetectionCattle\r\n"
        p = DailyParser(header_line)

        adsm_iteration_output = ["1,1,1"]

        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], DailyByProductionType)
        self.assertEqual(results[0].firstDetection, 1)

    def test_parse_single_field_in_daily_by_zone_and_production_type(self):
        cattle = ProductionType.objects.create(name="Cattle")
        medium_risk = Zone.objects.create(name="Medium Risk", radius=5.0)
        header_line = "Run,Day,unitsInZoneMediumRiskCattle\r\n"
        p = DailyParser(header_line)

        adsm_iteration_output = ["1,1,1"]

        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], DailyByZoneAndProductionType)
        self.assertEqual(results[0].unitsInZone, 1)

    def test_parse_multiple_fields_in_same_table(self):
        cattle = ProductionType.objects.create(name="Cattle")
        medium_risk = Zone.objects.create(name="Medium Risk", radius=5.0)
        header_line = "Run,Day,unitsInZoneMediumRiskCattle,animalDaysInZoneMediumRiskCattle\r\n"
        p = DailyParser(header_line)

        adsm_iteration_output = ["1,1,1,2"]

        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], DailyByZoneAndProductionType)
        self.assertEqual(results[0].unitsInZone, 1)
        self.assertEqual(results[0].animalDaysInZone, 2)

    def test_parse_multiple_fields_in_different_tables(self):
        cattle = ProductionType.objects.create(name="Cattle")
        medium_risk = Zone.objects.create(name="Medium Risk", radius=5.0)
        header_line = "Run,Day,firstDetectionCattle,animalDaysInZoneMediumRiskCattle\r\n"
        p = DailyParser(header_line)

        adsm_iteration_output = ["1,1,1,2"]

        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 2)

        result = [result for result in results if type(result) == DailyByProductionType]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].firstDetection, 1)

        result = [result for result in results if type(result) == DailyByZoneAndProductionType]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].animalDaysInZone, 2)

    def test_parse_single_field_background_zone(self):
        """
            the background zone is used if no other zone is specified
            it will not exist in the ScenarioCreator Zone table so it will
            not have a foreign key in the Results DailyByZone table
        """
        header_line = "Run,Day,zoneAreaBackground\r\n"
        p = DailyParser(header_line)

        adsm_iteration_output = ["1,1,1"]

        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], DailyByZone)
        self.assertEqual(results[0].zone, None)
        self.assertEqual(results[0].zoneArea, 1)

    def test_parse_unknown_column(self):
        header_line = "Run,Day,aaaaaa\r\n"
        p = DailyParser(header_line)

        adsm_iteration_output = ["1,1,1"]

        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 0)
        self.assertEqual(len(p.failures), 1)
        self.assertEqual(p.failures, {'aaaaaa'})

    def test_parser_only_outputs_needed_objects(self):
        """
            the results parser should not output an object if all
            fields of that object are None
        """
        # cattle = ProductionType.objects.create(name="Cattle")

        header_line = "Run,Day,outbreakDuration\r\n"
        p = DailyParser(header_line)

        adsm_iteration_output = ["1,1,1"]

        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], DailyControls)
