from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
import unittest
import os

from django.test import TestCase

from ScenarioCreator.models import AirborneSpread
from ScenarioCreator.views import workspace_path


class AirborneSpreadTestCase(TestCase):
    multi_db = True

    def setUp(self):
        self.form_data = {
            'name': 'Test',
            'spread_1km_probability': '0.5',
            'max_distance': '2',
            'exposure_direction_start': '0',
            'exposure_direction_end': '360',
        }

    def test_get(self):
        r = self.client.get('/setup/AirborneSpread/new/')

        self.assertEqual(r.status_code, 200)
        self.assertIn("Create a new Airborne Spread", r.content)

    def test_post_success(self):
        count = AirborneSpread.objects.count()
        r = self.client.post('/setup/AirborneSpread/new/', self.form_data)

        self.assertRedirects(r, '/setup/AirborneSpread/')
        self.assertEqual(count + 1, AirborneSpread.objects.count())

    def test_post_failure(self):
        del self.form_data['name']

        r = self.client.post('/setup/AirborneSpread/new/', self.form_data)

        self.assertContains(r, 'This field is required.', count=1, status_code=200)

class ScenarioTestCase(TestCase):
    multi_db = True

    def remove_test_file(self, file_path):
        try:
            os.remove(file_path)
        except:
            pass

    def test_post_success(self):
        file_name = 'Test Scenario 123 AZ'
        file_path = workspace_path(file_name) + '.sqlite3'

        self.remove_test_file(file_path)

        r = self.client.post('/setup/SaveScenario/', {'filename': file_name}, follow=True)

        try:
            self.assertRedirects(r, '/setup/Scenario/new/')
            self.assertTrue(os.path.isfile(file_path))
        finally:
            self.remove_test_file(file_path)

    def test_post_failure(self):
        file_name = 'Test \/ Scenario 123 AZ' # this should break Windows and Linux
        file_path = workspace_path(file_name) + '.sqlite3'

        self.remove_test_file(file_path)

        r = self.client.post('/setup/SaveScenario/', {'filename': file_name})

        try:
            self.assertContains(r, 'Failed to save file.', count=1, status_code=200)
            self.assertFalse(os.path.isfile(file_path))
        finally:
            self.remove_test_file(file_path)
