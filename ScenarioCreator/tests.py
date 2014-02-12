from django.test import TestCase

# Create your tests here.
class CreatorTest(TestCase):
    def test_index_page(self):
        r = self.client.get('/setup/')
        self.assertEqual(r.status_code, 200)

    def test_create_scenario(self):
        r = self.client.get('/setup/new/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('form' in r.context)
        r = self.client.post('/setup/new/', {'description':'words', "naadsm-version":'3.2.19', "language":'en',
                                             "num-runs":'10', "num-days":'40', 'scenario-name':'sample'})#TODO complete top level spec
        #"exit-condition":...
        self.assertEqual(r.status_code, 200)
