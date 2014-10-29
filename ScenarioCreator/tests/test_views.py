from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
import unittest
import os
import json
import tempfile

from django.test import TestCase

from ScenarioCreator.models import (AirborneSpread, RelationalFunction,
        RelationalPoint, ProbabilityFunction, DiseaseProgression)

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
        self.assertIn('Create a new Airborne Spread', r.content.decode())

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
        with open(POPULATION_FIXTURES + 'Population_Test_Invalid.xml', mode='rb') as fp:
            r = self.client.post('/setup/UploadPopulation/', {'file': fp})

        data = json.loads(r.content.decode())
        self.assertEqual(data, expected_results)

class RelationalFunctionTestCase(TestCase):
    multi_db = True

    def test_list(self):
        r = self.client.get('/setup/Function/')

        self.assertEqual(r.status_code, 200)
        self.assertIn('Create Functions', r.content.decode())

    def test_get(self):
        function = RelationalFunction.objects.create(name="Test Function")

        r = self.client.get('/setup/RelationalFunction/%d/' % function.pk)

        self.assertEqual(r.status_code, 200)
        self.assertIn('title', r.context)
        self.assertEqual('Create a Relational Function', r.context['title'])
        self.assertIn('Test Function', r.content.decode())

    def test_post_no_points(self):
        form_data = {
            'relationalpoint_set-TOTAL_FORMS': '0',
            'relationalpoint_set-INITIAL_FORMS': '0',
            'relationalpoint_set-MAX_NUM_FORMS': '1',
            'name': 'Test Function',
            'x_axis_units': 'Days',
        }
        r = self.client.post('/setup/RelationalFunction/new/', form_data, follow=True)

        self.assertEqual(RelationalFunction.objects.count(), 1)
        function = RelationalFunction.objects.first()
        self.assertEqual(function.name, 'Test Function')
        self.assertRedirects(r, '/setup/RelationalFunction/%d/' % function.pk)

    def test_post_with_points(self):
        form_data = {
            'relationalpoint_set-TOTAL_FORMS': '1',
            'relationalpoint_set-INITIAL_FORMS': '0',
            'relationalpoint_set-MAX_NUM_FORMS': '1',
            'relationalpoint_set-0-x': '0.0',
            'relationalpoint_set-0-y': '1.0',
            'name': 'Test Function',
            'x_axis_units': 'Days',
        }
        r = self.client.post('/setup/RelationalFunction/new/', form_data, follow=True)

        self.assertEqual(RelationalFunction.objects.count(), 1)
        function = RelationalFunction.objects.first()
        self.assertEqual(RelationalPoint.objects.count(), 1)
        point = RelationalPoint.objects.first()
        self.assertEqual(point.relational_function, function)
        self.assertEqual(point.x, 0.0)
        self.assertEqual(point.y, 1.0)
        self.assertEqual(function.name, 'Test Function')
        self.assertRedirects(r, '/setup/RelationalFunction/%d/' % function.pk)

    def test_copy_no_points(self):
        form_data = {
            'relationalpoint_set-TOTAL_FORMS': '0',
            'relationalpoint_set-INITIAL_FORMS': '0',
            'relationalpoint_set-MAX_NUM_FORMS': '1',
            'name': 'Test Function',
            'x_axis_units': 'Days',
        }
        function = RelationalFunction.objects.create(name="Test Function")

        r = self.client.post('/setup/RelationalFunction/%d/copy/' % function.pk, form_data)

        self.assertEqual(RelationalFunction.objects.count(), 2)
        qs = RelationalFunction.objects.filter(name='Test Function')
        qs = qs.exclude(pk=function.pk)
        self.assertEqual(qs.count(), 1)
        new_function = qs.first()

        self.assertRedirects(r, '/setup/RelationalFunction/%d/' % new_function.pk)

    def test_copy_with_points(self):
        form_data = {
            'relationalpoint_set-TOTAL_FORMS': '1',
            'relationalpoint_set-INITIAL_FORMS': '0',
            'relationalpoint_set-MAX_NUM_FORMS': '1',
            'relationalpoint_set-0-x': '0.0',
            'relationalpoint_set-0-y': '1.0',
            'name': 'Test Function',
            'x_axis_units': 'Days',
        }
        function = RelationalFunction.objects.create(name="Test Function")
        point = RelationalPoint.objects.create(x=0.0, y=1.0, relational_function=function)

        r = self.client.post('/setup/RelationalFunction/%d/copy/' % function.pk, form_data)

        self.assertEqual(RelationalFunction.objects.count(), 2)
        qs = RelationalFunction.objects.filter(name='Test Function')
        qs = qs.exclude(pk=function.pk)
        self.assertEqual(qs.count(), 1)
        new_function = qs.first()

        self.assertEqual(RelationalPoint.objects.count(), 2)
        new_point = RelationalPoint.objects.get(relational_function=new_function)
        self.assertNotEqual(new_point.pk, point.pk)
        self.assertEqual(new_point.x, point.x)
        self.assertEqual(new_point.y, point.y)

        self.assertRedirects(r, '/setup/RelationalFunction/%d/' % new_function.pk)

    def test_post_with_points_from_file(self):
        points_file = tempfile.NamedTemporaryFile(delete=False)
        points_file.write(b"x,y\n0.0, 1.0\n")
        points_file.seek(0)
        form_data = {
            'relationalpoint_set-TOTAL_FORMS': '0',
            'relationalpoint_set-INITIAL_FORMS': '0',
            'relationalpoint_set-MAX_NUM_FORMS': '1',
            'name': 'Test Function',
            'x_axis_units': 'Days',
            'file': points_file
        }
        r = self.client.post('/setup/RelationalFunction/new/', form_data, follow=True)

        self.assertEqual(RelationalFunction.objects.count(), 1)
        function = RelationalFunction.objects.first()
        self.assertEqual(function.name, 'Test Function')
        self.assertEqual(RelationalPoint.objects.count(), 1)
        point = RelationalPoint.objects.first()
        self.assertEqual(point.x, 0.0)
        self.assertEqual(point.y, 1.0)
        self.assertRedirects(r, '/setup/RelationalFunction/%d/' % function.pk)

        points_file.close()
        os.unlink(points_file.name)

    def test_related_objects_exist(self):
        relational_function = RelationalFunction.objects.create(name="Test Function")
        probability_function = ProbabilityFunction.objects.create(name="Test Probability Function")
        disease_progression = DiseaseProgression.objects.create(
            name="Test Progression",
            disease_latent_period=probability_function,
            disease_subclinical_period=probability_function,
            disease_clinical_period=probability_function,
            disease_immune_period=probability_function,
            disease_prevalence=relational_function)
        progression_url = '/setup/DiseaseProgression/%d/' % disease_progression.pk

        r = self.client.get('/setup/RelationalFunction/%d/' % relational_function.pk)

        self.assertIn('backlinks', r.context)
        self.assertIn('Test Progression', r.context['backlinks'])
        self.assertEqual(progression_url, r.context['backlinks']['Test Progression'])