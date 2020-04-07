import unittest
from django.core.exceptions import ValidationError
from django.test import TestCase, TransactionTestCase
from ADSMSettings.utils import workspace_path

from ScenarioCreator.models import (Scenario, choice_char_from_value, squish_name,
                                    Unit, Population, ProductionType, IndirectSpread,
                                    ProbabilityDensityFunction, RelationalFunction, Disease,
                                    VaccinationGlobal, OutputSettings)
from ScenarioCreator.population_parser import PopulationParser
from ScenarioCreator.forms import IndirectSpreadForm
from ADSMSettings.models import SingletonManager

updatedPost = {'description': 'Updated Description',
               "naadsm_version": '3.2.19', "language": 'en', "num_runs": '10',
               "num_days": '40', 'scenario_name': 'sample'}
standardPost = {'description': 'words', "naadsm_version": '3.2.19',
                "language": 'en', "num_runs": '10',
                "num_days": '40', 'scenario_name': 'sample'}


class CreatorTest(TestCase):
    multi_db = True

    def test_index_page(self):
        r = self.client.get('')
        self.assertEqual(r.status_code, 302)
        self.assertIn('loading_url=/app/Startup/', r.url)
        r = self.client.get(r.url)
        self.assertTemplateUsed('LoadingScreen.html')


    def test_index_page_with_loading_url(self):
        r = self.client.get('/LoadingScreen/', {'loading_url': 'app/Workspace/'})
        self.assertEqual(r.status_code, 200)
        self.assertIn('loading_url', r.context)
        self.assertEqual(r.context['loading_url'], 'app/Workspace/')


    def test_create_Scenario(self):
        r = self.client.get('/setup/Scenario/new/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('form' in r.context)
        length = Scenario.objects.count()
        r = self.client.post('/setup/Scenario/new/', standardPost)
        #"exit_condition":...
        self.assertEqual(r.status_code, 200)  #returns content to edit page on post of new content
        self.assertEqual(Scenario.objects.count(), length + 1)

    def test_edit_Scenario(self):
        r = self.client.post('/setup/Scenario/new/', standardPost)
        r = self.client.get('/setup/Scenario/1/')
        r = self.client.post('/setup/Scenario/1/', updatedPost)
        self.assertEqual(Scenario.objects.get().description, 'Updated Description')


class ModelUtilsTest(TestCase):
    multi_db = True

    def test_choice_char_from_value(self):
        choices = Unit._meta.get_field_by_name('initial_state')[0]._choices
        tests = ['Vaccine immune', 'destroyed', '  Latent', 'SubClinical', 'kittens']
        results = [choice_char_from_value(x, choices) for x in tests]
        self.assertListEqual(results, ['V','D','L','B',None])

    def test_squish(self):
        self.assertEqual('thefeanciestevar', squish_name('  The FeanCiest Evar  '))

    def test_population_source_file_invalid(self):
        p = Population(source_file='Population_Grid.xml')
        with self.assertRaises(OSError):
            p.save()

    def test_population_removes_itself_when_errors_occur(self):
        population_count = Population.objects.all().count()
        p = Population(source_file='Population_Grid.xml')
        with self.assertRaises(OSError):
            p.save()
        self.assertEqual(population_count, Population.objects.all().count())

    def test_population_source_file_blank(self):
        unit_count = Unit.objects.all().count()
        p = Population(source_file='')

        p.save()

        self.assertEqual(unit_count, Unit.objects.all().count())

    def test_population_link(self):
        from ScenarioCreator.tests.test_parser import POPULATION_FIXTURES
        index = Unit.objects.count()
        p = Population(source_file=POPULATION_FIXTURES + 'Population_Grid.xml')
        p.save()

        new_unit = p.unit_set.first()
        self.assertGreater( Unit.objects.count(), index, "No new Units were added")
        self.assertEqual( Unit.objects.get(id=new_unit.id)._population, p, "New Unit should link back to newest Population object")


class IndirectSpreadFormTestCase(TestCase):
    multi_db = True

    def setUp(self):
        self.p_f = ProbabilityDensityFunction.objects.create(name="Test PF", equation_type="Triangular")
        self.r_f = RelationalFunction.objects.create(name="Test RF")

        self.form_data = {
            'name': 'Test',
            'contact_rate': '0.1',
            'infection_probability': '0.5',
            'distance_distribution': self.p_f.pk,
            'movement_control': self.r_f.pk
        }

    def test_indirect_spread(self):
        form = IndirectSpreadForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_indirect_spread_probability_error(self):
        self.form_data['infection_probability'] = '2'
        form = IndirectSpreadForm(data=self.form_data)

        self.assertFalse(form.is_valid())

        self.assertIn('infection_probability', form.errors)


class CleanTest(TestCase):
    multi_db = True

    def test_production_type_names(self):
        pt = ProductionType(name='Bob')
        pt.clean_fields()
        pt = ProductionType(name='Bob,')
        self.assertRaises(ValidationError, pt.clean_fields)
        pt = ProductionType(name='TABLE')
        self.assertRaises(ValidationError, pt.clean_fields)
        pt = ProductionType(name='table')
        self.assertRaises(ValidationError, pt.clean_fields)


class ViewTests(TransactionTestCase):
    multi_db = True

    def test_delete_links_exist(self):
        self.client.get('/app/OpenTestScenario/ScenarioCreator/tests/population_fixtures/Roundtrip.db/')

        r = self.client.get('/setup/Populations/')
        self.assertIn('data-delete-link', r.content.decode())

        r = self.client.get('/setup/DiseaseProgression/')
        self.assertIn('data-delete-link', r.content.decode())

        r = self.client.get('/setup/DiseaseSpread/')
        self.assertIn('data-delete-link', r.content.decode())

        r = self.client.get('/setup/ControlProtocol/')
        self.assertIn('data-delete-link', r.content.decode())

        r = self.client.get('/setup/Zone/')
        self.assertIn('data-delete-link', r.content.decode())

        r = self.client.get('/setup/ZoneEffect/')
        self.assertIn('data-delete-link', r.content.decode())

        # has a related model, not deleteable
        function = RelationalFunction.objects.get(name="Prevalence")
        r = self.client.get('/setup/RelationalFunction/%s/' % function.id)
        self.assertNotIn('data-delete-link', r.content.decode())

        # has no related models, deleteable
        function = RelationalFunction.objects.create(name="Test RelationalFunction")
        r = self.client.get('/setup/RelationalFunction/%s/' % function.id)
        self.assertIn('data-delete-link', r.content.decode())


class PopulationTestCase(TestCase):
    multi_db = True

    def test_model_is_singleton(self):
        self.assertIsInstance(Population.objects, SingletonManager)

    def test_save(self):
        result = Population()
        result.id = 2
        result.save()

        result = Population.objects.get()
        self.assertEqual(Population.objects.count(), 1)
        self.assertEqual(result.pk, 1)


class VaccinationGlobalTestCase(TestCase):
    multi_db = True

    def test_model_is_singleton(self):
        self.assertIsInstance(VaccinationGlobal.objects, SingletonManager)

    def test_save(self):
        result = VaccinationGlobal()
        result.id = 2
        result.save()

        result = VaccinationGlobal.objects.get()
        self.assertEqual(VaccinationGlobal.objects.count(), 1)
        self.assertEqual(result.pk, 1)


class DiseaseTestCase(TestCase):
    multi_db = True

    def test_model_is_singleton(self):
        self.assertIsInstance(Disease.objects, SingletonManager)

    def test_save(self):
        result = Disease()
        result.id = 2
        result.save()

        result = Disease.objects.get()
        self.assertEqual(Disease.objects.count(), 1)
        self.assertEqual(result.pk, 1)


class ScenarioTestCase(TestCase):
    multi_db = True

    def test_model_is_singleton(self):
        self.assertIsInstance(Scenario.objects, SingletonManager)

    def test_save(self):
        result = Scenario()
        result.id = 2
        result.save()

        result = Scenario.objects.get()
        self.assertEqual(Scenario.objects.count(), 1)
        self.assertEqual(result.pk, 1)


class OutputSettingsTestCase(TestCase):
    multi_db = True

    def test_model_is_singleton(self):
        self.assertIsInstance(OutputSettings.objects, SingletonManager)

    def test_save(self):
        result = OutputSettings()
        result.id = 2
        result.save()

        result = OutputSettings.objects.get()
        self.assertEqual(OutputSettings.objects.count(), 1)
        self.assertEqual(result.pk, 1)

 
'''
Testing all of the functions from db_status_tags.py.
Tests present in this class = 8
'''
class StatusTags(TestCase):
    multi_db = True

    #takes in an expected "target_address" and a "url" and tests if they are equal while ignoring case-sensitive characters.
    #returns "active " for good match and "" for bad.
    def test_active(self):
        #expected URL
        target_address = "@@@.My test url.###"

        #two test cases, one for a good match and one for bad.
        self.assertEqual("active ", db_status_tags.active(target_address, "@@@.my Test Url.###"))
        self.assertEqual("", db_status_tags.active(target_address, "Invalid URL"))

    #complete takes a boolean type parameter and returns "completed " for True and "incomplete" for false
    def test_complete(self):

        #two test cases, one for true and one for false
        self.assertEqual("completed ", db_status_tags.completed(True))
        self.assertEqual("incomplete", db_status_tags.completed(False))

    #parent_link() function is present in db_status_tags but currently has no uses in program, no testing required.
    def test_parent_link(self):
        return


    #action_id() takes a given string and replaces '/' with '-'
    def test_action_id(self):
        #test text
        text = "Testing/This/Text"
        #running the text through the action_id() function
        formatted = db_status_tags.action_id(text)

        self.assertEqual("Testing-This-Text", formatted)

    #takes string and optional url and returns a django SafeString HTML link with the works linked to a url
    def test_wiki(self):
        test_string = "My Test String"
        test_url = "@@@.MyFakeURL.###"

        #three test, one for each of the folling cases:
            #url is not provided
            #url == "/"
            #url is provided
        #the following list cooriponds to the above cases and marks what the URL is parsed out to be without the HTML
            #https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#my-test-string
            #https://github.com/NAVADMC/ADSM/wiki/
            #https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#@@@.MyFakeURL.###

        #case 1
        self.assertEqual('<a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#my-test-string" class="wiki" target="_blank">My Test String</a>',
                         db_status_tags.wiki(test_string))
        #case 2
        self.assertEqual('<a href="https://github.com/NAVADMC/ADSM/wiki/" class="wiki" target="_blank">My Test String</a>',
                         db_status_tags.wiki(test_string, url = "/"))
        #case 3
        self.assertEqual('<a href="https://github.com/NAVADMC/ADSM/wiki/Lexicon-of-Disease-Spread-Modelling-terms#@@@.MyFakeURL.###" class="wiki" target="_blank">My Test String</a>',
                         db_status_tags.wiki(test_string, url = test_url))

    #bold() takes an input string ("words") and returns a django SafeString surrounded by HTML <strong> tags.
    def test_bold(self):
        #starting text
        to_bold = "Test Text"
        #bold the text
        bolded = db_status_tags.bold(to_bold)

        #test against expected return
        self.assertEqual("<strong>Test Text</strong>", bolded)

    #link() takes in words and a url link and returns a django SafeString HTML link with the words linked to the text
    def test_link(self):
        #test url
        url = "@@@.fakelink.###"
        #test text
        words = "Test Link"
        #combining the two using the link() function
        html = db_status_tags.link(words, url)

        #test against expected return
        self.assertEqual('<a href="@@@.fakelink.###" class="wiki" target="_blank">Test Link</a>',html)

    #form_completed() function is present in db_status_tags but currently has no uses in program, no testing required.
    def test_form_completed(self):
        return
