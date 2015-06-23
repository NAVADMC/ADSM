import unittest
from django.core.exceptions import ValidationError
from django.test import TestCase, TransactionTestCase
from ADSMSettings.utils import workspace_path

from ScenarioCreator.models import (Scenario, choice_char_from_value, squish_name,
                                    Unit, Population, ProductionType, IndirectSpread,
                                    ProbabilityFunction, RelationalFunction, Disease,
                                    ControlMasterPlan, OutputSettings)
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
        tests = ['Vaccine immune', 'destroyed', '  Latent', 'Infectious SubClinical', 'kittens']
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
        index = Unit.objects.count()
        p = Population(source_file=workspace_path('Population_Grid.xml'))
        p.save()

        new_unit = p.unit_set.first()
        self.assertGreater( Unit.objects.count(), index, "No new Units were added")
        self.assertEqual( Unit.objects.get(id=new_unit.id)._population, p, "New Unit should link back to newest Population object")


class IndirectSpreadFormTestCase(TestCase):
    multi_db = True

    def setUp(self):
        self.p_f = ProbabilityFunction.objects.create(name="Test PF", equation_type="Triangular")
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
        self.client.get('/app/OpenTestScenario/ScenarioCreator/tests/population_fixtures/Roundtrip.sqlite3/')

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


class ControlMasterPlanTestCase(TestCase):
    multi_db = True

    def test_model_is_singleton(self):
        self.assertIsInstance(ControlMasterPlan.objects, SingletonManager)

    def test_save(self):
        result = ControlMasterPlan()
        result.id = 2
        result.save()

        result = ControlMasterPlan.objects.get()
        self.assertEqual(ControlMasterPlan.objects.count(), 1)
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
