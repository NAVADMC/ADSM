from django.test import TestCase

# Create your tests here.
from ScenarioCreator.models import Ingeneral

updatedPost = {'description': 'Updated Description', "naadsm_version": '3.2.19', "language": 'en', "num_runs": '10',
     "num_days": '40', 'scenario_name': 'sample'}
standardPost = {'description': 'words', "naadsm_version": '3.2.19', "language": 'en', "num_runs": '10',
                        "num_days": '40', 'scenario_name': 'sample'}

class CreatorTest(TestCase):
    def test_index_page(self):
        r = self.client.get('/setup/')
        self.assertEqual(r.status_code, 200)

    def test_create_Ingeneral(self):
        r = self.client.get('/setup/new/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('form' in r.context)
        length = Ingeneral.objects.count()
        r = self.client.post('/setup/new/', standardPost)
        #"exit_condition":...
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Ingeneral.objects.count(), length +1)

    def test_edit_Ingeneral(self):
        r = self.client.post('/setup/new/', standardPost)
        r = self.client.get('/setup/1/')
        r = self.client.post('/setup/1/', updatedPost)
        self.assertEqual(Ingeneral.objects.get(pk=1).description, 'Updated Description')

