import unittest
import os
import json
import tempfile

from django.test import TestCase

from ScenarioCreator.models import (AirborneSpread, RelationalFunction,
        RelationalPoint, ProbabilityFunction, DiseaseProgression,
        ProductionType, Zone, ZoneEffect, ZoneEffectAssignment)
from ADSMSettings.utils import workspace_path
from ADSM import settings

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
        self.assertIn('Spread 1km probability', r.content.decode())

    def test_post_success(self):
        count = AirborneSpread.objects.count()
        r = self.client.post('/setup/AirborneSpread/new/', self.form_data)
        self.assertEqual(r.status_code, 200)
        
        r = self.client.get('/setup/AirborneSpread/')
        self.assertIn('Test', r.content.decode())
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
            'message': "This is not a valid Population file: "+'mismatched tag: line 17, column 2'
        }
        try:
            os.remove(workspace_path('Population_Test_Invalid.xml'),)
        except OSError: pass
        with open(POPULATION_FIXTURES + 'Population_Test_Invalid.xml', mode='rb') as fp:
            r = self.client.post('/setup/UploadPopulation/', {'file': fp})

        # data = json.loads(r.content.decode())
        self.assertJSONEqual(r.content.decode(), expected_results)

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
        self.assertIn('/setup/RelationalFunction/%d/' % function.pk, r.content.decode())

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
        self.assertIn('/setup/RelationalFunction/%d/' % function.pk, r.content.decode())

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

        html_response = r.content.decode()
        print(html_response)
        self.assertIn('/setup/RelationalFunction/%d/' % new_function.pk, html_response)

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

        self.assertIn('/setup/RelationalFunction/%d/' % new_function.pk, r.content.decode())

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

        temp_file_name = os.path.basename(points_file.name)
        temp_file_upload_path = workspace_path(temp_file_name)
        self.assertFalse(os.path.exists(temp_file_upload_path))

        self.assertEqual(RelationalFunction.objects.count(), 1)
        function = RelationalFunction.objects.first()
        self.assertEqual(function.name, 'Test Function')
        self.assertEqual(RelationalPoint.objects.count(), 1)
        point = RelationalPoint.objects.first()
        self.assertEqual(point.x, 0.0)
        self.assertEqual(point.y, 1.0)
        self.assertIn('/setup/RelationalFunction/%d/' % function.pk, r.content.decode())

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

class AssignEffectsTestCase(TestCase):
    multi_db = True

    def setUp(self):
        self.client.get('/setup/AirborneSpread/new/')

    def test_does_not_error_on_new_scenario(self):
        r = self.client.get('/setup/AssignZoneEffects/')
        self.assertEqual(r.status_code, 200)

    def test_does_not_error_with_population_but_no_zones(self):
        with open(POPULATION_FIXTURES + 'Population_Test_Zone_Assignment.xml', mode='rb') as fp:
            self.client.post('/setup/UploadPopulation/', {'file': fp})

        r = self.client.get('/setup/AssignZoneEffects/')
        self.assertEqual(r.status_code, 200)

    def test_does_not_error_with_no_zone_effects(self):
        with open(POPULATION_FIXTURES + 'Population_Test_Zone_Assignment.xml', mode='rb') as fp:
            self.client.post('/setup/UploadPopulation/', {'file': fp, 'overwrite_ok':'overwrite_ok'})
        pt_1 = ProductionType.objects.get(name="Free Range Cows")
        Zone.objects.create(name="A", radius=2)
        Zone.objects.create(name="B", radius=4)

        r = self.client.get('/setup/AssignZoneEffects/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['formset_grouped'][pt_1]), 2)

    def test_correctly_initializes_formsets_with_partial_ZoneEffectAssignments(self):
        with open(POPULATION_FIXTURES + 'Population_Test_Zone_Assignment.xml', mode='rb') as fp:
            self.client.post('/setup/UploadPopulation/', {'file': fp, 'overwrite_ok':'overwrite_ok'})
        pt_1 = ProductionType.objects.get(name="Free Range Cows")
        pt_2 = ProductionType.objects.get(name="Dairy Cows")
        zone_a = Zone.objects.create(name="A", radius=2)
        zone_b = Zone.objects.create(name="B", radius=4)
        effect_1 = ZoneEffect.objects.create(name="1")
        effect_2 = ZoneEffect.objects.create(name="2")
        ZoneEffectAssignment.objects.create(zone=zone_a, production_type=pt_1, effect=effect_1)
        ZoneEffectAssignment.objects.create(zone=zone_a, production_type=pt_2, effect=effect_2)

        r = self.client.get('/setup/AssignZoneEffects/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.context['formset_grouped']), ProductionType.objects.count())
        self.assertEqual(len(r.context['formset_grouped'][pt_1]), 2)
        self.assertEqual(r.context['formset_grouped'][pt_1][0].instance.id, 1)
        self.assertEqual(r.context['formset_grouped'][pt_1][0].instance.effect, effect_1)

    def test_save_ZoneEffectAssignment(self):
        with open(POPULATION_FIXTURES + 'Population_Test_Zone_Assignment.xml', mode='rb') as fp:
            self.client.post('/setup/UploadPopulation/', {'file': fp, 'overwrite_ok':'overwrite_ok'})
        pt_1 = ProductionType.objects.get(name="Free Range Cows")
        pt_2 = ProductionType.objects.get(name="Dairy Cows")
        zone_a = Zone.objects.create(name="A", radius=2)
        zone_b = Zone.objects.create(name="B", radius=4)
        effect_1 = ZoneEffect.objects.create(name="1")
        effect_2 = ZoneEffect.objects.create(name="2")
        updated_zone_effect = ZoneEffectAssignment.objects.create(zone=zone_a, production_type=pt_1, effect=effect_1)
        ZoneEffectAssignment.objects.create(zone=zone_a, production_type=pt_2, effect=effect_2)

        form_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form-MAX_NUM_FORMS': '1',
            'form-0-id': updated_zone_effect.pk,
            'form-0-effect': effect_2.pk,
        }

        r = self.client.post('/setup/AssignZoneEffects/', form_data, follow=True)

        self.assertEqual(r.status_code, 200)
        updated_zone_effect = ZoneEffectAssignment.objects.get(pk=updated_zone_effect.pk)
        self.assertEqual(updated_zone_effect.effect, effect_2)
