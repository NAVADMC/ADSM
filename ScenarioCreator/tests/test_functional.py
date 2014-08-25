import time

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from ScenarioCreator.models import Scenario, Disease, DiseaseProgression, ProbabilityFunction, RelationalFunction

class FunctionalTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(FunctionalTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(FunctionalTests, cls).tearDownClass()

    def test_edit_probability_via_modal(self):
        self.selenium.get('%s' % self.live_server_url)
        time.sleep(1)

        lp_cattle = ProbabilityFunction.objects.create(name="Latent period - cattle", equation_type="Triangular", min=0, mode=3, max=9)
        sp_cattle = ProbabilityFunction.objects.create(name="Subclinical period - cattle", equation_type="Triangular", min=1, mode=3, max=5)
        cp_cattle = ProbabilityFunction.objects.create(name="Clinical period - cattle", equation_type="Triangular", min=0, mode=21, max=80)
        ip_cattle = ProbabilityFunction.objects.create(name="Immune Period", equation_type="Triangular", min=180, mode=270, max=360)
        fmd = Disease.objects.create(name='FMD', disease_description=u'Foot and Mouth Disease')
        disease_progression = DiseaseProgression.objects.create(_disease=fmd,
            name='Cattle Reaction',
            disease_latent_period=lp_cattle,
            disease_subclinical_period=sp_cattle,
            disease_clinical_period=cp_cattle,
            disease_immune_period=ip_cattle)

        self.selenium.find_element_by_tag_name('nav').find_element_by_link_text('Disease Progression').click()
        time.sleep(1)

        self.selenium.find_element_by_link_text('Cattle Reaction').click()
        time.sleep(1)

        self.selenium.find_element_by_id('div_id_disease_latent_period').find_element_by_tag_name('i').click()
        time.sleep(1)

        modal = self.selenium.find_element_by_id('disease_latent_period_modal')
        modal.find_element_by_id('id_name').send_keys(' edited')
        for button in modal.find_elements_by_tag_name('button'):
            if button.text == 'Save changes':
                button.click()
        time.sleep(1)

        with self.assertRaises(NoSuchElementException):
            self.selenium.find_element_by_id('disease_latent_period_modal')

        lp_cattle = ProbabilityFunction.objects.get(pk=lp_cattle.pk)
        self.assertEqual(lp_cattle.name, "Latent period - cattle edited")

    def test_upload_population_file(self):
        self.selenium.get('%s' % self.live_server_url)
        time.sleep(1)

        self.selenium.find_element_by_tag_name('nav').find_element_by_link_text('Population').click()
        time.sleep(1)

        self.selenium.find_element_by_link_text('Population_Grid.xml').click()
        time.sleep(3) # may need to be adjusted for slow computers or if the file grows

        section = self.selenium.find_element_by_tag_name('section')
        self.assertIn('Current Units:', section.text)

    def test_upload_blank_population_file(self):
        self.selenium.get('%s' % self.live_server_url)
        time.sleep(1)

        self.selenium.find_element_by_tag_name('nav').find_element_by_link_text('Population').click()
        time.sleep(1)

        self.selenium.find_element_by_link_text('Blank.xml').click()
        time.sleep(3) # may need to be adjusted for slow computers or if the file grows

        section = self.selenium.find_element_by_tag_name('section')
        self.assertIn('Current Units:', section.text)
