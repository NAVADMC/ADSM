from django.test import TestCase

# Create your tests here.
from ScenarioCreator.models import Scenario, choice_char_from_value, squish_name, Unit

updatedPost = {'description': 'Updated Description', "naadsm_version": '3.2.19', "language": 'en', "num_runs": '10',
               "num_days": '40', 'scenario_name': 'sample'}
standardPost = {'description': 'words', "naadsm_version": '3.2.19', "language": 'en', "num_runs": '10',
                "num_days": '40', 'scenario_name': 'sample'}


class CreatorTest(TestCase):
    def test_index_page(self):
        r = self.client.get('/setup/')
        self.assertEqual(r.status_code, 200)

    def test_create_Scenario(self):
        r = self.client.get('/setup/new/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('form' in r.context)
        length = Scenario.objects.count()
        r = self.client.post('/setup/new/', standardPost)
        #"exit_condition":...
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Scenario.objects.count(), length +1)

    def test_edit_Scenario(self):
        r = self.client.post('/setup/new/', standardPost)
        r = self.client.get('/setup/1/')
        r = self.client.post('/setup/1/', updatedPost)
        self.assertEqual(Scenario.objects.get(pk=1).description, 'Updated Description')


class ModelUtilsTest(TestCase):
    def test_choice_char_from_value(self):
        choices = Unit._meta.get_field_by_name('initial_state')[0]._choices
        tests = ['Vaccine immune', 'destroyed', '  Latent', 'Infectious SubClinical', 'kittens']
        results = [choice_char_from_value(x, choices) for x in tests]
        self.assertListEqual(results, ['V','D','L','B',None])

    def test_squish(self):
        self.assertEqual('thefeanciestevar', squish_name('  The FeanCiest Evar  '))