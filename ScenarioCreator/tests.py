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
from ScenarioCreator.parser import PopulationParser

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

    def test_population_source_file_invalid(self):
        p = Population(source_file='Population_Grid.xml')
        with self.assertRaises(OSError):
            p.save()

    def test_population_source_file_blank(self):
        unit_count = Unit.objects.all().count()
        p = Population(source_file='')

        p.save()

        self.assertEqual(unit_count, Unit.objects.all().count())

    def test_population_link(self):
        index = Unit.objects.count()
        p = Population(source_file='workspace/Population_Grid.xml')
        p.save()
        self.assertGreater( Unit.objects.count(), index, "No new Units were added")
        self.assertEqual( Unit.objects.get(id=index+1)._population, p, "New Unit should link back to newest Population object")


class PopulationParserTestCase(TestCase):
    def test_parser_load_invalid_file(self):
        with self.assertRaises(OSError):
            PopulationParser('Invalid_File.xml')

    def test_parser_load_blank_file(self):
        with self.assertRaises(EOFError) as e:
            p = PopulationParser('workspace/Blank.xml')

        self.assertEqual(str(e.exception), "File Read returned a blank string.")

    def test_parser_load_utf8(self):
        expected_results = {
            'user_notes': '1',
            'initial_size': '84',
            'latitude': '52.9672',
            'longitude': '-8.201',
            'production_type': 'B',
            'initial_state': 'Susceptible',
        }
        p = PopulationParser('workspace/Population_Test_UTF8.xml')

        results = p.parse_to_dictionary()

        self.assertEqual(len(results), 1)
        self.assertDictEqual(results[0], expected_results)

    def test_parser_load_utf16(self):
        expected_results = {
            'user_notes': '\u5f71\u97ff\u3092\u53d7\u3051\u3084\u3059\u3044',
            'initial_size': '84',
            'latitude': '52.9672',
            'longitude': '-8.201',
            'production_type': 'B',
            'initial_state': 'Susceptible',
        }
        p = PopulationParser('workspace/Population_Test_UTF16.xml')

        results = p.parse_to_dictionary()

        self.assertEqual(len(results), 1)
        self.assertDictEqual(results[0], expected_results)

    def test_parser_multiple_herds(self):
        expected_results = [
            {
                'user_notes': '1',
                'initial_size': '84',
                'latitude': '52.9672',
                'longitude': '-8.201',
                'production_type': 'B',
                'initial_state': 'Susceptible',
            },
            {
                'user_notes': '2',
                'initial_size': '64',
                'latitude': '52.9672',
                'longitude': '-8.21',
                'production_type': 'B',
                'initial_state': 'Susceptible',
            },
        ]

        p = PopulationParser('workspace/Population_Test_Multiple.xml')

        results = p.parse_to_dictionary()

        self.assertEqual(len(results), 2)
        self.assertDictEqual(results[0], expected_results[0])
        self.assertDictEqual(results[1], expected_results[1])


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


