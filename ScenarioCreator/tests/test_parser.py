from xml.etree.ElementTree import ParseError

from django.test import TestCase

# Create your tests here.
from ADSMSettings.utils import workspace_path
from ScenarioCreator.models import Scenario, choice_char_from_value, squish_name, Unit, Population, ProductionType
from ScenarioCreator.population_parser import PopulationParser

POPULATION_FIXTURES = 'ScenarioCreator/tests/population_fixtures/'


class PopulationParserTestCase(TestCase):
    multi_db = True

    def test_parser_load_invalid_file(self):
        with self.assertRaises(OSError):
            PopulationParser('Invalid_File.xml')

    def test_parser_load_blank_file(self):
        with self.assertRaises(EOFError) as e:
            p = PopulationParser(workspace_path('Blank.xml'))

        self.assertEqual(str(e.exception), "File Read returned a blank string.")

    def test_parser_load_utf8(self):
        expected_results = {
            'user_notes': 'id=1',
            'initial_size': '100',
            'latitude': '50',
            'longitude': '-8',
            'production_type': 'Free Range Cows',
            'initial_state': 'Susceptible',
        }
        p = PopulationParser(POPULATION_FIXTURES + 'Population_Test_UTF8.xml')

        results = p.parse_to_dictionary()

        self.assertEqual(len(results), 8)
        self.assertDictEqual(results[0], expected_results)

    def test_parser_load_utf16(self):
        expected_results = {
            'user_notes': 'id=\u5f71\u97ff\u3092\u53d7\u3051\u3084\u3059\u3044',
            'initial_size': '84',
            'latitude': '52.9672',
            'longitude': '-8.201',
            'production_type': 'B',
            'initial_state': 'Susceptible',
        }
        p = PopulationParser(POPULATION_FIXTURES + 'Population_Test_UTF16.xml')

        results = p.parse_to_dictionary()

        self.assertEqual(len(results), 1)
        self.assertDictEqual(results[0], expected_results)

    def test_parser_multiple_herds(self):
        expected_results = [
            {
                'user_notes': 'id=1',
                'initial_size': '84',
                'latitude': '52.9672',
                'longitude': '-8.201',
                'production_type': 'B',
                'initial_state': 'Susceptible',
            },
            {
                'user_notes': 'id=2',
                'initial_size': '64',
                'latitude': '52.9672',
                'longitude': '-8.21',
                'production_type': 'B',
                'initial_state': 'Susceptible',
            },
        ]

        p = PopulationParser(POPULATION_FIXTURES + 'Population_Test_Multiple.xml')

        results = p.parse_to_dictionary()

        self.assertEqual(len(results), 2)
        self.assertDictEqual(results[0], expected_results[0])
        self.assertDictEqual(results[1], expected_results[1])

    def test_parser_load_invalid_xml(self):
        with self.assertRaises(ParseError):
            PopulationParser(POPULATION_FIXTURES + 'Population_Test_Invalid.xml')
