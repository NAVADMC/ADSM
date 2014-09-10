from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
import unittest

from django.test import TestCase

from ScenarioCreator.forms import AirborneSpreadForm

class AirborneSpreadTestCase(TestCase):

    def setUp(self):
        self.form_data = {
            'name': 'Test',
            'spread_1km_probability': '0.5',
            'max_distance': '2',
            'exposure_direction_start': '0',
            'exposure_direction_end': '360',
        }

    def test_valid(self):
        form = AirborneSpreadForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_name_required(self):
        error_text = "This field is required."
        del self.form_data['name']

        form = AirborneSpreadForm(data=self.form_data)

        self.assertIn('name', form.errors)
        self.assertIn(error_text, form.errors['name'])

    def test_probability_required(self):
        error_text = "This field is required."
        del self.form_data['spread_1km_probability']

        form = AirborneSpreadForm(data=self.form_data)

        self.assertIn('spread_1km_probability', form.errors)
        self.assertIn(error_text, form.errors['spread_1km_probability'])

    def test_invalid_probability_low(self):
        error_text = "Ensure this value is greater than or equal to 0.0."
        self.form_data['spread_1km_probability'] = '-1'

        form = AirborneSpreadForm(data=self.form_data)

        self.assertIn('spread_1km_probability', form.errors)
        self.assertIn(error_text, form.errors['spread_1km_probability'])

    def test_invalid_probability_high(self):
        error_text = "Ensure this value is less than or equal to 0.999."
        self.form_data['spread_1km_probability'] = '1'

        form = AirborneSpreadForm(data=self.form_data)

        self.assertIn('spread_1km_probability', form.errors)
        self.assertIn(error_text, form.errors['spread_1km_probability'])

    def test_max_distance_low(self):
        error_text = "Ensure this value is greater than or equal to 1.1."
        self.form_data['max_distance'] = '1'

        form = AirborneSpreadForm(data=self.form_data)

        self.assertIn('max_distance', form.errors)
        self.assertIn(error_text, form.errors['max_distance'])

    def test_invalid_exposure_start_low(self):
        error_text = "Ensure this value is greater than or equal to 0."
        self.form_data['exposure_direction_start'] = '-1'

        form = AirborneSpreadForm(data=self.form_data)

        self.assertIn('exposure_direction_start', form.errors)
        self.assertIn(error_text, form.errors['exposure_direction_start'])

    def test_invalid_exposure_start_high(self):
        error_text = "Ensure this value is less than or equal to 360."
        self.form_data['exposure_direction_start'] = '361'

        form = AirborneSpreadForm(data=self.form_data)

        self.assertIn('exposure_direction_start', form.errors)
        self.assertIn(error_text, form.errors['exposure_direction_start'])

    def test_invalid_exposure_end_low(self):
        error_text = "Ensure this value is greater than or equal to 0."
        self.form_data['exposure_direction_end'] = '-1'

        form = AirborneSpreadForm(data=self.form_data)

        self.assertIn('exposure_direction_end', form.errors)
        self.assertIn(error_text, form.errors['exposure_direction_end'])

    def test_invalid_exposure_end_end(self):
        error_text = "Ensure this value is less than or equal to 360."
        self.form_data['exposure_direction_end'] = '361'

        form = AirborneSpreadForm(data=self.form_data)

        self.assertIn('exposure_direction_end', form.errors)
        self.assertIn(error_text, form.errors['exposure_direction_end'])
