from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
import unittest
import os
import json

from django.test import TestCase

from ScenarioCreator.models import AirborneSpread

POPULATION_FIXTURES = 'ScenarioCreator/tests/population_fixtures/'


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

class PopulationTestCase(TestCase):
    multi_db = True

    def test_post_failure_bad_xml(self):
        expected_results = {
            'status': 'failed',
            'message': 'mismatched tag: line 17, column 2'
        }
        with open(POPULATION_FIXTURES + 'Population_Test_Invalid.xml') as fp:
            r = self.client.post('/setup/UploadPopulation/', {'file': fp})

        data = json.loads(r.content)
        self.assertEqual(data, expected_results)
