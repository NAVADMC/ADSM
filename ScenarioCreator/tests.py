from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
import unittest
from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from ScenarioCreator.models import Scenario, choice_char_from_value, squish_name, Unit, Population, ProductionType

updatedPost = {'description': 'Updated Description', "naadsm_version": '3.2.19', "language": 'en', "num_runs": '10',
               "num_days": '40', 'scenario_name': 'sample'}
standardPost = {'description': 'words', "naadsm_version": '3.2.19', "language": 'en', "num_runs": '10',
                "num_days": '40', 'scenario_name': 'sample'}


class CreatorTest(TestCase):
    def test_index_page(self):
        r = self.client.get('')
        self.assertEqual(r.status_code, 302)

    def test_create_Scenario(self):
        r = self.client.get('/setup/Scenario/new/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('form' in r.context)
        length = Scenario.objects.count()
        r = self.client.post('/setup/Scenario/new/', standardPost)
        #"exit_condition":...
        self.assertEqual(r.status_code, 302)  #redirects to edit page on post of new content
        self.assertEqual(Scenario.objects.count(), length + 1)

    def test_edit_Scenario(self):
        r = self.client.post('/setup/Scenario/new/', standardPost)
        r = self.client.get('/setup/Scenario/1/')
        r = self.client.post('/setup/Scenario/1/', updatedPost)
        self.assertEqual(Scenario.objects.get(pk=1).description, 'Updated Description')


class ModelUtilsTest(TestCase):
    def test_choice_char_from_value(self):
        choices = Unit._meta.get_field_by_name('initial_state')[0]._choices
        tests = ['Vaccine immune', 'destroyed', '  Latent', 'Infectious SubClinical', 'kittens']
        results = [choice_char_from_value(x, choices) for x in tests]
        self.assertListEqual(results, ['V','D','L','B',None])

    def test_squish(self):
        self.assertEqual('thefeanciestevar', squish_name('  The FeanCiest Evar  '))

    def test_population_link(self):
        index = Unit.objects.count()
        p = Population(source_file='Population_Grid.xml')
        p.save()
        self.assertGreater( Unit.objects.count(), index, "No new Units were added")
        self.assertEqual( Unit.objects.get(id=index+1)._population, p, "New Unit should link back to newest Population object")

class CleanTest(unittest.TestCase):
    def test_production_type_names(self):
        pt = ProductionType(name='Bob')
        pt.clean_fields()
        pt = ProductionType(name='123Bob')
        self.assertRaises(ValidationError, pt.clean_fields)
        pt = ProductionType(name='Bob@#$%^&*')
        self.assertRaises(ValidationError, pt.clean_fields)
        pt = ProductionType(name='TABLE')
        self.assertRaises(ValidationError, pt.clean_fields)
        pt = ProductionType(name='table')
        self.assertRaises(ValidationError, pt.clean_fields)


