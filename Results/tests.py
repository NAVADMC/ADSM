from django.test import TestCase, TransactionTestCase
from django.db import connections, close_old_connections
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
from ADSMSettings.models import scenario_filename


class SimulationTest(TransactionTestCase):
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
        close_old_connections()

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
        close_old_connections()
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
        close_old_connections()
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
        close_old_connections()
        file_name = os.path.join(self.scenario_directory, 'Roundtrip_test Map Output.zip')
        folder_name = os.path.join(self.scenario_directory, 'Map')

        sim = Simulation(1)
        sim.start()
        sim.join()

        self.assertFalse(os.access(file_name, os.F_OK))


class IterationProgressTestClass(TestCase):
    multi_db = True
    
    def setUp(self):
        self.settings, created = OutputSettings.objects.get_or_create(iterations=10)

    def test_no_iterations_completed(self):
        iteration = 10
        days = 7
        for i in range(1, iteration + 1):
            for d in range(1, days + 1):
                last_day = d == days
                DailyControls.objects.create(iteration=i, day=d, last_day=last_day)
        self.assertEqual(iteration_progress(), 0.05)

    def test_two_iterations_completed_disease_end(self):
        self.settings.stop_criteria = "disease-end"
        self.settings.save()
        iteration = 10
        days = 7
        for i in range(1, iteration + 1):
            for d in range(1, days + 1):
                DailyControls.objects.create(iteration=i, day=d)
            if i <= 8:
                DailyControls.objects.create(iteration=i, day=8, diseaseDuration=8, last_day=True)
        self.assertEqual(iteration_progress(), 0.8)

    def test_two_iterations_completed_first_detection(self):
        self.settings.stop_criteria = "first-detection"
        self.settings.save()
        pigs, created = ProductionType.objects.get_or_create(name="pig")
        cats, created = ProductionType.objects.get_or_create(name="cat")
        iteration = 10
        days = 7
        for i in range(1, iteration + 1):
            for d in range(1, days + 1):
                DailyControls.objects.create(iteration=i, day=d)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=None)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=pigs)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=cats)
            if i <= 6:
                DailyControls.objects.create(iteration=i, day=8, diseaseDuration=8, last_day=True)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=None, firstDetection=1, last_day=True)
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=pigs, firstDetection=1, last_day=True) # first detection happened in pigs
                DailyByProductionType.objects.create(iteration=i, day=d, production_type=cats, last_day=True)
        self.assertEqual(iteration_progress(), 0.6)

    def test_two_iterations_completed_outbreak_end(self):
        self.settings.stop_criteria = "outbreak-end"
        self.settings.save()
        iteration = 10
        days = 7
        for i in range(1, iteration + 1):
            for d in range(1, days + 1):
                DailyControls.objects.create(iteration=i, day=d)
            if i <= 4:
                DailyControls.objects.create(iteration=i, day=8, outbreakDuration=8, last_day=True)
        self.assertEqual(iteration_progress(), 0.4)

    def test_two_iterations_completed_stop_days(self):
        self.settings.stop_criteria = "stop-days"
        self.settings.days = 8
        self.settings.save()
        iteration = 10
        days = 7
        for i in range(1, iteration + 1):
            for d in range(1, days + 1):
                DailyControls.objects.create(iteration=i, day=d)
            if i <= 2:
                DailyControls.objects.create(iteration=i, day=8, last_day=True)
        self.assertEqual(iteration_progress(), 0.2)


class ParserTests(TestCase):
    multi_db = True

    def setUp(self):
        self.production_types = [(1, "Cattle")]
        self.zones = [(1, "Medium Risk")]
        self.common_headers = "Run,Day,versionMajor,versionMinor,versionRelease"

    def test_initialize(self):
        header_line = self.common_headers + "\r\n"

        p = DailyParser(header_line, self.production_types, self.zones)

        self.assertEqual(p.headers, ['Run', 'Day', 'versionMajor', 'versionMinor', 'versionRelease'])
        self.assertEqual(p.possible_zones, {'Medium Risk', 'Background'})
        self.assertEqual(p.possible_pts, {'', 'Cattle'})

    def test_parse_single_field_in_controls(self):
        header_line = self.common_headers + ",outbreakDuration\r\n"
        p = DailyParser(header_line, self.production_types, self.zones)

        adsm_iteration_output = "1,1,3,2,1,1"
        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[1], DailyControls)
        self.assertEqual(results[1].outbreakDuration, 1)

    def test_parse_single_field_in_daily_by_production_type(self):
        header_line = self.common_headers + ",firstDetectionCattle\r\n"
        p = DailyParser(header_line, self.production_types, self.zones)

        adsm_iteration_output = "1,1,3,2,1,1"
        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[1], DailyByProductionType)
        self.assertEqual(results[1].firstDetection, 1)

    def test_parse_single_field_in_daily_by_zone_and_production_type(self):
        header_line = self.common_headers + ",unitsInZoneMediumRiskCattle\r\n"
        p = DailyParser(header_line, self.production_types, self.zones)
        adsm_iteration_output = "1,1,3,2,1,1"

        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[1], DailyByZoneAndProductionType)
        self.assertEqual(results[1].unitsInZone, 1)

    def test_parse_multiple_fields_in_same_table(self):
        header_line = self.common_headers + ",unitsInZoneMediumRiskCattle,animalDaysInZoneMediumRiskCattle\r\n"
        p = DailyParser(header_line, self.production_types, self.zones)

        adsm_iteration_output = "1,1,3,2,1,1,2"
        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[1], DailyByZoneAndProductionType)
        self.assertEqual(results[1].unitsInZone, 1)
        self.assertEqual(results[1].animalDaysInZone, 2)

    def test_parse_multiple_fields_in_different_tables(self):
        header_line = self.common_headers + ",firstDetectionCattle,animalDaysInZoneMediumRiskCattle\r\n"
        p = DailyParser(header_line, self.production_types, self.zones)
        adsm_iteration_output = "1,1,3,2,1,1,2"
        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 3)

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
        header_line = self.common_headers + ",zoneAreaBackground\r\n"
        p = DailyParser(header_line, self.production_types, self.zones)
        adsm_iteration_output = "1,1,3,2,1,1"
        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[1], DailyByZone)
        self.assertEqual(results[1].zone, None)
        self.assertEqual(results[1].zoneArea, 1)

    def test_parse_unknown_column(self):
        header_line = self.common_headers + ",aaaaaa\r\n"
        p = DailyParser(header_line, self.production_types, self.zones)
        adsm_iteration_output = "1,1,3,2,1,1"
        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 1)
        self.assertEqual(len(p.failures), 1)
        self.assertEqual(p.failures, {'aaaaaa'})

    def test_parser_only_outputs_needed_objects(self):
        """
            the results parser should not output an object if all
            fields of that object are None
        """
        header_line = self.common_headers + ",outbreakDuration\r\n"
        p = DailyParser(header_line, self.production_types, self.zones)
        adsm_iteration_output = "1,1,3,2,19,1"
        results = p.parse_daily_strings(adsm_iteration_output)

        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[1], DailyControls)
