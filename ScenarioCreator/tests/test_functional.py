import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from ScenarioCreator.models import Scenario, Disease, DiseaseProgression, \
    ProbabilityFunction, RelationalFunction, RelationalPoint, Population, \
    DirectSpread, IndirectSpread, AirborneSpread, ProductionType, \
    DiseaseProgressionAssignment, Unit


class M2mDSL(object):
    """
        DSL to improve m2m widget tests readability
    """
    def click_navbar_element(self, name, sleep=1):
        target = self.selenium.find_element_by_tag_name('nav')
        target.find_element_by_link_text(name).click()
        time.sleep(sleep)

    def click_production_type(self, name, type_of_type='source'):
        row_selector = 'section > div > table > tbody > tr'
        source_type_selector = 'th:first-of-type span'
        destination_type_selector = 'th:nth-of-type(2) span'

        rows = self.selenium.find_elements_by_css_selector(row_selector)
        for row in rows:
            if type_of_type == 'source':
                target = row.find_element_by_css_selector(source_type_selector)
            elif type_of_type == 'destination':
                target = row.find_element_by_css_selector(destination_type_selector)
            if target.text == name:
                target.click()

    def click_button(self, name, type_of_type='source', sleep=1):
        row_selector = 'section > div > table > thead > tr:nth-of-type(2)'
        source_selector = 'td:first-of-type button'
        destination_selector = 'td:nth-of-type(2) button'

        row = self.selenium.find_element_by_css_selector(row_selector)
        if type_of_type == 'source':
            buttons = row.find_elements_by_css_selector(source_selector)
        elif type_of_type == 'destination':
            buttons = row.find_elements_by_css_selector(destination_selector)
        for button in buttons:
            if button.text == name:
                button.click()
                time.sleep(sleep)
                break

    def select_bulk_contact_disease(self, name, sleep=1):
        target = self.selenium.find_element_by_id("id_bulk-direct_contact_spread")
        Select(target).select_by_visible_text(name)
        time.sleep(sleep)

    def select_contact_disease(self, name, sleep=2):
        select_selector = 'section > div > table > tbody > tr:first-of-type > td:first-of-type select'
        target = self.selenium.find_element_by_css_selector(select_selector)
        Select(target).select_by_visible_text(name)
        time.sleep(sleep)

    def get_bulk_production_types(self):
        row_selector = 'section > div > table > tbody > tr'
        source_selector = 'th:first-of-type span'
        select_selector = 'td:first-of-type select'
        rows = self.selenium.find_elements_by_css_selector(row_selector)

        production_types = []
        for row in rows:
            source = row.find_element_by_css_selector(source_selector)
            select = Select(row.find_element_by_css_selector(select_selector))
            production_type = {}
            production_type['source'] = source.text
            production_type['disease'] = select.first_selected_option.text
            production_types.append(production_type)

        return production_types

    def get_interactions(self):
        row_selector = 'form > table > tbody > tr'
        source_selector = 'select[id$="source_production_type"]'
        destination_selector = 'select[id$="destination_production_type"]'
        disease_selector = 'select[id$="-direct_contact_spread"]'

        rows = self.selenium.find_elements_by_css_selector(row_selector)

        interactions = []
        for row in rows:
            source_select = Select(row.find_element_by_css_selector(source_selector))
            destination_select = Select(row.find_element_by_css_selector(destination_selector))
            disease_select = Select(row.find_element_by_css_selector(disease_selector))
            interaction = {}
            interaction['source'] = source_select.first_selected_option.text
            interaction['destination'] = destination_select.first_selected_option.text
            interaction['disease'] = disease_select.first_selected_option.text
            interactions.append(interaction)

        return interactions

    def get_selected_production_types(self, type_of_type='source'):
        row_selector = 'section > div > table > tbody'
        source_selector = 'th:first-of-type span.selected'
        destination_selector = 'th:nth-of-type(2) span.selected'

        rows = self.selenium.find_element_by_css_selector(row_selector)
        if type_of_type == 'source':
            return rows.find_elements_by_css_selector(source_selector)
        elif type_of_type == 'destination':
            return rows.find_elements_by_css_selector(destination_selector)


class FunctionalTests(LiveServerTestCase, M2mDSL):
    multi_db = True

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Chrome()
        super(FunctionalTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(FunctionalTests, cls).tearDownClass()

    def setUp(self):
        # do this first to cause initial database migrations to occur
        self.selenium.get(self.live_server_url)
        time.sleep(1)

    def setup_scenario(self):
        """ handle all temp object creation for tests """
        population = Population.objects.create(source_file="ScenarioCreator/tests/population_fixtures/Population_Test_UTF8.xml")
        lp_cattle = ProbabilityFunction.objects.create(name="Latent period - cattle", equation_type="Triangular", min=0, mode=3, max=9)
        sp_cattle = ProbabilityFunction.objects.create(name="Subclinical period - cattle", equation_type="Triangular", min=1, mode=3, max=5)
        cp_cattle = ProbabilityFunction.objects.create(name="Clinical period - cattle", equation_type="Triangular", min=0, mode=21, max=80)
        ip_cattle = ProbabilityFunction.objects.create(name="Immune Period", equation_type="Triangular", min=180, mode=270, max=360)
        dcd = ProbabilityFunction.objects.create(name="Direct contact distance", x_axis_units="Kilometers", equation_type="Triangular", min=10, mode=20, max=30)
        idcd = ProbabilityFunction.objects.create(name="Indirect contact distance", x_axis_units="Kilometers", equation_type="Triangular", min=20, mode=40, max=60)
        um = RelationalFunction.objects.create(name="Unrestricted movement", x_axis_units="Days", y_axis_units="Percentage")
        RelationalPoint.objects.create(relational_function=um, x=0, y=1)
        RelationalPoint.objects.create(relational_function=um, x=100000, y=1)
        fmd = Disease.objects.create(name='FMD', disease_description=u'Foot and Mouth Disease')
        prevalence = RelationalFunction.objects.create(name="Prevalence", x_axis_units="Days", y_axis_units="Percentage")
        RelationalPoint.objects.create(relational_function=prevalence, x=0, y=1)
        disease_progression = DiseaseProgression.objects.create(_disease=fmd,
            name='Cattle Reaction',
            disease_latent_period=lp_cattle,
            disease_subclinical_period=sp_cattle,
            disease_clinical_period=cp_cattle,
            disease_immune_period=ip_cattle,
            disease_prevalence=prevalence)
        production_type = ProductionType.objects.get(name="Free Range Cows")
        assigned_type = DiseaseProgressionAssignment.objects.create(production_type=production_type,
            progression=disease_progression)
        dc_ds1 = DirectSpread.objects.create(name="Dairy Cattle Large",
            latent_animals_can_infect_others=True,
            contact_rate=5,
            infection_probability=1,
            distance_distribution=dcd,
            movement_control=um)
        dc_ds2 = DirectSpread.objects.create(name="Dairy Cattle Small",
            latent_animals_can_infect_others=True,
            contact_rate=0.5,
            infection_probability=1,
            distance_distribution=dcd,
            movement_control=um)
        ids1 = IndirectSpread.objects.create(name="Dairy Cattle Large",
            contact_rate=5,
            infection_probability=1,
            distance_distribution=idcd,
            movement_control=um)
        ids2 = IndirectSpread.objects.create(name="Dairy Cattle Small",
            contact_rate=0.5,
            infection_probability=1,
            distance_distribution=idcd,
            movement_control=um)
        as1 = AirborneSpread.objects.create(name="Dairy Cattle Large",
            spread_1km_probability=0.1,
            wind_direction_start=0,
            wind_direction_end=360,
            max_distance=3)
        as2 = AirborneSpread.objects.create(name="Dairy Cattle Small",
            spread_1km_probability=0.05,
            wind_direction_start=0,
            wind_direction_end=360,
            max_distance=3)

    def test_edit_probability_via_modal(self):
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
        self.selenium.find_element_by_tag_name('nav').find_element_by_link_text('Population').click()
        time.sleep(1)

        self.selenium.find_element_by_link_text('Population_Grid.xml').click()
        time.sleep(3) # may need to be adjusted for slow computers or if the file grows

        section = self.selenium.find_element_by_tag_name('section')
        self.assertIn('Current Units:', section.text)

    def test_upload_blank_population_file(self):
        self.selenium.find_element_by_tag_name('nav').find_element_by_link_text('Population').click()
        time.sleep(1)

        self.selenium.find_element_by_link_text('Blank.xml').click()
        time.sleep(3) # may need to be adjusted for slow computers or if the file grows

        section = self.selenium.find_element_by_tag_name('section')
        self.assertIn('Load a Population', section.text)

        alert = self.selenium.find_element_by_class_name('alert')
        self.assertIn('Error: File Read returned a blank string.', alert.text)

    def test_delete_population(self):
        population = Population.objects.create(source_file="ScenarioCreator/tests/population_fixtures/Population_Test_UTF8.xml")

        self.click_navbar_element('Population')

        # javascript is attaching to this event
        self.selenium.find_element_by_css_selector('[data-delete-link]').click()
        time.sleep(2)

        modal = self.selenium.find_element_by_class_name('bootstrap-dialog')

        self.assertIn("Delete Confirmation", modal.text)
        self.assertIn("Are you sure you want to delete the selected Population?", modal.text)

        for button in modal.find_elements_by_tag_name('button'):
            if button.text == "Delete":
                button.click()
                break

        time.sleep(2)

        section = self.selenium.find_element_by_tag_name('section')
        self.assertIn('Load a Population', section.text)

    def test_delete_unit(self):
        population = Population.objects.create(source_file="ScenarioCreator/tests/population_fixtures/Population_Test_UTF8.xml")
        old_count = Unit.objects.count()

        self.click_navbar_element('Population')

        self.selenium.find_element_by_id('id_form-0-DELETE').click()
        self.selenium.find_element_by_id('submit-id-submit').click()
        time.sleep(2)

        self.assertEqual(old_count - 1, Unit.objects.count())

    def test_assign_disease_spread_layout(self):
        self.setup_scenario()

        self.selenium.find_element_by_tag_name('nav') \
            .find_element_by_link_text('Assign Disease Spread').click()
        time.sleep(2)

        m2m_widget = self.selenium.find_element_by_css_selector('section > div > table')

        # check that the buttons are present
        buttons = m2m_widget.find_elements_by_tag_name('button')
        self.assertEqual(len([b for b in buttons if b.text == "Select All"]), 2)
        self.assertEqual(len([b for b in buttons if b.text == "Deselect All"]), 2)
        self.assertEqual(len([b for b in buttons if b.text == "Apply"]), 3)

        # and production type labels
        self.assertEqual(m2m_widget.text.count("Free Range Cows"), 2)
        self.assertEqual(m2m_widget.text.count("Dairy Cows"), 2)
        self.assertEqual(m2m_widget.text.count("Angus Cattle"), 2)
        self.assertEqual(m2m_widget.text.count("Blue Horn"), 2)

        # and selects
        selects = m2m_widget.find_elements_by_tag_name('select')
        self.assertEqual(len(selects), 15)

    def test_assign_disease_spread_bulk_operator_default(self):
        """
            bulk operator applies disease spreads to interactions
            with the same production type for source and destination
        """
        self.setup_scenario()
        self.click_navbar_element("Assign Disease Spread")

        self.select_bulk_contact_disease("Dairy Cattle Large 1")

        # verify bulk selector for each destination production type were updated
        types = self.get_bulk_production_types()
        for production_type in types:
            self.assertEqual(production_type['disease'], "Dairy Cattle Large 1")

        # verify interactions are set correctly
        interactions = self.get_interactions()
        for interaction in interactions:
            if interaction['source'] == interaction['destination']:
                self.assertEqual(interaction['disease'], 'Dairy Cattle Large 1')
            else:
                self.assertEqual(interaction['disease'], u'---------')

    def test_assign_disease_spread_bulk_operator_single_source_selected(self):
        """
            bulk operator applies disease spreads to all interactions
            with the same source production type for source selected
        """
        self.setup_scenario()
        self.click_navbar_element("Assign Disease Spread")

        self.click_production_type("Free Range Cows")
        self.select_bulk_contact_disease("Dairy Cattle Large 1")

        # verify bulk selector for each destination production type were updated
        types = self.get_bulk_production_types()
        for production_type in types:
            self.assertEqual(production_type['disease'], "Dairy Cattle Large 1")

        interactions = self.get_interactions()
        for interaction in interactions:
            if interaction['source'] == 'Free Range Cows':
                self.assertEqual(interaction['disease'], "Dairy Cattle Large 1")
            else:
                self.assertEqual(interaction['disease'], u"---------")

    def test_assign_disease_spread_bulk_operator_multiple_sources_selected(self):
        """
            bulk operator applies disease spreads to interactions
            with the same source production types for source selected
        """
        self.setup_scenario()
        self.click_navbar_element("Assign Disease Spread")

        self.click_production_type("Free Range Cows")
        self.click_production_type("Dairy Cows")
        self.select_bulk_contact_disease("Dairy Cattle Large 1")

        # verify bulk selector for each destination production type were updated
        types = self.get_bulk_production_types()
        for production_type in types:
            self.assertEqual(production_type['disease'], "Dairy Cattle Large 1")

        interactions = self.get_interactions()
        for interaction in interactions:
            if (interaction['source'] == 'Free Range Cows' or
                    interaction['source'] == 'Dairy Cows'):
                self.assertEqual(interaction['disease'], "Dairy Cattle Large 1")
            else:
                self.assertEqual(interaction['disease'], u"---------")

    def test_assign_disease_spread_bulk_operator_multiple_sources_and_destinations_selected(self):
        """
            bulk operator applies disease spreads to interactions
            with the same source production types and destination types
            for source selected
        """
        self.setup_scenario()
        self.click_navbar_element("Assign Disease Spread")

        self.click_production_type("Free Range Cows")
        self.click_production_type("Dairy Cows")
        self.click_production_type("Free Range Cows", "destination")
        self.click_production_type("Dairy Cows", "destination")
        self.select_bulk_contact_disease("Dairy Cattle Large 1")

        # verify bulk selector for each destination production type were updated
        types = self.get_bulk_production_types()
        for production_type in types:
            if (production_type['source'] == "Free Range Cows" or
                production_type['source'] == "Dairy Cows"):
                # only the sources selected should have updated
                self.assertEqual(production_type['disease'], "Dairy Cattle Large 1")
            else:
                self.assertEqual(production_type['disease'], u"---------")

        interactions = self.get_interactions()
        for interaction in interactions:
            i = interaction
            if ((i['source'] == 'Free Range Cows' or i['source'] == 'Dairy Cows') and
                (i['destination'] == 'Free Range Cows' or i['destination'] == 'Dairy Cows')):
                # both the source and destination type were selected
                self.assertEqual(interaction['disease'], "Dairy Cattle Large 1")
            else:
                self.assertEqual(interaction['disease'], u"---------")

    def test_assign_disease_spread_select_all_button_source(self):
        """
            clicking the select all button for sources in the m2m widget
            will cause all production types to be selected
        """
        self.setup_scenario()
        self.click_navbar_element("Assign Disease Spread")

        self.click_button("Select All")

        source_types = self.get_selected_production_types()
        self.assertEqual(len(source_types), 4)

    def test_assign_disease_spread_select_all_button_destination(self):
        """
            clicking the select all button for destinations in the m2m widget
            will cause all production types to be selected
        """
        self.setup_scenario()
        self.click_navbar_element("Assign Disease Spread")

        self.click_button("Select All", "destination")

        selected_types = self.get_selected_production_types("destination")
        self.assertEqual(len(selected_types), 4)

    def test_assign_disease_spread_deselect_all_button_source(self):
        self.setup_scenario()
        self.click_navbar_element("Assign Disease Spread")
        self.click_production_type("Free Range Cows")
        self.click_production_type("Dairy Cows")
        self.click_production_type("Angus Cattle")
        self.click_production_type("Blue Horn")

        self.click_button("Deselect All")

        source_types = self.get_selected_production_types()
        self.assertEqual(len(source_types), 0)

    def test_assign_disease_spread_deselect_all_button_destination(self):
        self.setup_scenario()
        self.click_navbar_element("Assign Disease Spread")
        self.click_production_type("Free Range Cows", "destination")
        self.click_production_type("Dairy Cows", "destination")
        self.click_production_type("Angus Cattle", "destination")
        self.click_production_type("Blue Horn", "destination")

        self.click_button("Deselect All", "destination")

        source_types = self.get_selected_production_types("destination")
        self.assertEqual(len(source_types), 0)

    def test_assign_disease_spread_add_disease_modal(self):
        self.setup_scenario()
        self.click_navbar_element("Assign Disease Spread")
        self.select_contact_disease("Add...")

        modal = self.selenium.find_element_by_css_selector('div[id$="-direct_contact_spread_modal"]')

        self.assertIn("Create a new Direct Spread", modal.text)

    def test_modal_hide_unneeded_probability_fields(self):
        """
            issue 146: unneeded probability fields are not hidden in modals
        """
        self.setup_scenario()
        self.click_navbar_element("Assign Progression")

        target = self.selenium.find_elements_by_class_name('glyphicon-pencil')[0].click()
        time.sleep(2)

        modal = self.selenium.find_element_by_css_selector('div[id$="-progression_modal"]')

        modal.find_elements_by_class_name('glyphicon-pencil')[0].click()
        time.sleep(2)

        modal_2 = self.selenium.find_element_by_css_selector('div[id$="disease_latent_period_modal"]')

        mean_field = modal_2.find_element_by_id("div_id_mean")

        self.assertIn("none", mean_field.value_of_css_property("display"))
