from unittest import skip
from django.test import TestCase
import os
import json
from ScenarioCreator.models import DirectSpread

from ScenarioCreator.views import workspace_path
from .models import SmSession, SingletonManager
from .views import import_legacy_scenario


class ScenarioTestCase(TestCase):
    multi_db = True

    def remove_test_file(self, file_path):
        try:
            os.remove(file_path)
        except:
            print("Failed to delete", file_path)

    def test_post_success(self):
        file_name = 'Test Scenario 123 AZ.sqlite3'
        file_path = workspace_path(file_name)

        self.remove_test_file(file_path)

        r = self.client.post('/app/SaveScenario/', {'filename': file_name})

        try:
            self.assertEqual(r.status_code, 302)
            self.assertTrue(os.path.isfile(file_path))
        finally:
            pass
        #     self.remove_test_file(file_path)

    def test_post_failure_ajax(self):
        file_name = 'Test \/ Scenario 123 AZ' # this should break Windows and Linux
        file_path = workspace_path(file_name) + '.sqlite3'

        self.remove_test_file(file_path)

        r = self.client.post('/app/SaveScenario/',
                             {'filename': file_name},
                             HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        try:
            html_r = r.content.decode()
            self.assertIn('Failed', html_r)
            self.assertIn('Slashes are not allowed: Test \\/ Scenario 123 AZ', html_r)
            self.assertFalse(os.path.isfile(file_path))
        finally:
            self.remove_test_file(file_path)


class SmSessionTestCase(TestCase):
    multi_db = True

    def test_model_is_singleton(self):
        self.assertIsInstance(SmSession.objects, SingletonManager)

    def test_save(self):
        result = SmSession()
        result.id = 2
        result.save()

        result = SmSession.objects.get()
        self.assertEqual(SmSession.objects.count(), 1)
        self.assertEqual(result.pk, 1)


class SingletonManagerTestCase(TestCase):
    multi_db = True

    def setUp(self):
        self.session = SmSession.objects.create(id=1, scenario_filename="Untitled Scenario")

    def test_get(self):
        result = SmSession.objects.get()
        
        self.assertEqual(result.pk, 1)

    def test_get_with_params(self):
        # why are we not raising DoesNotExist here?
        result = SmSession.objects.get(scenario_filename="Full Run")

        self.assertEqual(result.pk, 1)
        self.assertEqual(result.scenario_filename, "Full Run")

    def test_create(self):
        result = SmSession.objects.create(scenario_filename="Full Run")

        self.assertEqual(SmSession.objects.count(), 1)
        self.assertEqual(result.pk, self.session.pk)
        self.assertEqual(result.scenario_filename, "Full Run")

    def test_get_or_create_with_bad_id(self):
        result = SmSession.objects.get_or_create(id=2)

        self.assertEqual(SmSession.objects.count(), 1)
        self.assertEqual(result[0].pk, 1)

    def test_get_or_create_with_bad_pk(self):
        result = SmSession.objects.get_or_create(pk=2)

        self.assertEqual(SmSession.objects.count(), 1)
        self.assertEqual(result[0].pk, 1)

    def test_get_or_create_with_kwarg(self):
        result = SmSession.objects.get_or_create(scenario_filename="Full Run")

        self.assertEqual(SmSession.objects.count(), 1)
        self.assertEqual(result[0].scenario_filename, "Full Run")
        self.assertEqual(result[1], False)

    def test_get_or_create_without_existing_instance(self):
        self.session.delete()
        result = SmSession.objects.get_or_create()

        self.assertEqual(result[0].pk, 1)
        self.assertEqual(result[1], True)


class LegacyImporterTestCase(TestCase):
    multi_db = True

    @skip("This test isn't working because of a test-specific database connection problem")
    def test_import_sample_scenario(self):
        popul_path = r'"C:\Users\Josiah\Documents\ADSM\ScenarioCreator\tests\population_fixtures\export_pop.xml"'
        param_path = r'"C:\Users\Josiah\Documents\ADSM\ScenarioCreator\tests\population_fixtures\Sample_export.xml"'
        import_legacy_scenario(param_path, popul_path)
        
        print("DirectSpread.objects.count()", DirectSpread.objects.count())

# if __name__ == "__main__":
#     test_import_sample_scenario()
