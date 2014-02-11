from django.test import TestCase

# Create your tests here.
class CreatorTest(TestCase):
    def test_index_page(self):
        r = self.client.get('/setup/')
        self.assertEqual(r.status_code, 200)