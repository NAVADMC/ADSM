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
