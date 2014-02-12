from django.test import TestCase

# Create your tests here.
from ScenarioCreator.models import Scenario


class CreatorTest(TestCase):
    def test_index_page(self):
        r = self.client.get('/setup/')
        self.assertEqual(r.status_code, 200)

    def test_create_scenario(self):
        r = self.client.get('/setup/new/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('form' in r.context)
        length = Scenario.objects.count()
        r = self.client.post('/setup/new/', {'description':'words', "naadsm_version":'3.2.19', "language":'en',
                                             "num_runs":'10', "num_days":'40', 'scenario_name':'sample'})#TODO complete top level spec
        #"exit_condition":...
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Scenario.objects.count(), length +1)
