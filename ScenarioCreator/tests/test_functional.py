import glob
import time
import os
from unittest import skip
from django.conf import settings

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from ScenarioCreator.models import Scenario, Disease, DiseaseProgression, \
    ProbabilityFunction, RelationalFunction, RelationalPoint, Population, \
    DirectSpread, IndirectSpread, AirborneSpread, ProductionType, \
    DiseaseProgressionAssignment, Unit, ControlMasterPlan, Zone, ZoneEffect
from ADSMSettings.utils import workspace_path
from Results.utils import delete_all_outputs


def parent_of(webElement):
    return webElement.find_element_by_xpath('..')
    

class FunctionsPanel(object):
    """This class wraps the "#functions_panel" WebElement and adds some convenience methods. Kind of like Selenium's
    Select class that wraps drop-downs and adds convenience methods for selecting options."""
    def __init__(self, web_element, timeout=10):
        self.functions_panel = web_element
        # The parent of the WebElement object will be the WebDriver
        self.driver = web_element.parent
        self.actions = ActionChains(self.driver)
        self.timeout = timeout

    def _edit_with_overwrite(self):
        """Click the appropriate buttons to edit with overwrite."""
        WebDriverWait(self.functions_panel, timeout=self.timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'edit-button'))
        ).click()
        # You can get an "Other element would receive the click" exception if you try to click the Overwrite button
        # while the buttons are still animating into place. The animation takes 0.4 seconds (search for
        # .edit-button-holder in adsm.css).
        time.sleep(0.4)
        WebDriverWait(self.functions_panel, timeout=self.timeout).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'overwrite-button'))
        ).click()

    def _move_to_row(self, row):
        """Puts the focus on the x-point in the given row."""
        # We actually start on the y-point in that row, and tab backwards to get to the first x-point. That puts focus
        # on the x-point *and* selects whatever is currently filled in there, so that when we start typing, we'll
        # overwrite it.
        y_values = self.functions_panel.find_elements_by_xpath(".//input[starts-with(@name,'relationalpoint') and contains(@name,'-y')]")
        self.actions.move_to_element(y_values[row]).click().key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()

    def set_points(self, points):
        self._edit_with_overwrite()

        # Type in the points by tabbing between the fields like a user would do.
        self._move_to_row(0)
        first_point = True
        for x,y in points:
            if first_point:
                first_point = False
            else:
                # 2 tabs to go from Y -> Delete checkbox -> X on next row.
                self.actions.send_keys(Keys.TAB).send_keys(Keys.TAB).perform()
            self.actions.send_keys(str(x)).send_keys(Keys.TAB).send_keys(str(y)).perform()
        self.actions.send_keys(Keys.ENTER).perform() # just like clicking the Apply button

        # The blocking overlay will be up while the apply is perfomed
        WebDriverWait(self.driver, self.timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'blocking-overlay'))
        )

    def change_point(self, point_idx, new_point):
        self._edit_with_overwrite()

        self._move_to_row(point_idx)
        x, y = new_point
        if x is not None:
            self.actions.send_keys(str(x)).perform()
        if y is not None:
            self.actions.send_keys(Keys.TAB).send_keys(str(y)).perform()
        self.actions.send_keys(Keys.ENTER).perform() # just like clicking the Apply button

        # The blocking overlay will be up while the apply is perfomed
        WebDriverWait(self.driver, self.timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'blocking-overlay'))
        )

class FunctionalTests(StaticLiveServerTestCase):
    multi_db = True
    default_timeout = 10 # seconds
    tolerance = 1E-6 # small tolerance for floating-point comparison error

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Chrome()
        cls.selenium.set_window_size(1280, 800)
        super(FunctionalTests, cls).setUpClass()
        # if 'ADSMSettings/' not in glob.glob('*/'):
        #     raise NotADirectoryError("Tests started in the wrong directory! ", os.getcwd())
            # os.chdir('..') # go up a directory until you find the repo root

    @classmethod
    def tearDownClass(cls):
        cls.selenium.refresh()
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
        fmd = Disease.objects.create(name='FMD', disease_description=u'Foot and Mouth Disease', include_direct_contact_spread=True)
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
        self.dc_ds1 = DirectSpread.objects.create(name="Dairy Cattle Large",
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
            exposure_direction_start=0,
            exposure_direction_end=360,
            max_distance=3)
        as2 = AirborneSpread.objects.create(name="Dairy Cattle Small",
            spread_1km_probability=0.05,
            exposure_direction_start=0,
            exposure_direction_end=360,
            max_distance=3)
        zone = Zone.objects.create(name="Medium", radius=10)

    def click_navbar_element(self, name, sleep=1):
        target = WebDriverWait(self.selenium, self.default_timeout).until(
            EC.visibility_of_element_located((By.TAG_NAME, 'nav'))
        )
        target.find_element_by_link_text(name).click()
        time.sleep(sleep)

    def find(self, selector):
        return self.selenium.find_element_by_css_selector(selector)

    def select_option(self, element_id, visible_text, timeout=10):
        target = WebDriverWait(self.selenium, timeout).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        Select(target).select_by_visible_text(visible_text)
        time.sleep(2)  # wait for panel loading

    def test_edit_probability_in_progression(self):
        self.setup_scenario()

        lp_cattle = ProbabilityFunction.objects.create(name="Renaming Test - cattle", equation_type="Triangular", min=0, mode=3, max=9)
        sp_cattle = ProbabilityFunction.objects.create(name="Subclinical period - cattle", equation_type="Triangular", min=1, mode=3, max=5)
        cp_cattle = ProbabilityFunction.objects.create(name="Clinical period - cattle", equation_type="Triangular", min=0, mode=21, max=80)
        ip_cattle = ProbabilityFunction.objects.create(name="Immune Period", equation_type="Triangular", min=180, mode=270, max=360)
        fmd = Disease.objects.create(name='FMD', disease_description=u'Foot and Mouth Disease')
        disease_progression = DiseaseProgression.objects.create(_disease=fmd,
            name='Rename Test',
            disease_latent_period=lp_cattle,
            disease_subclinical_period=sp_cattle,
            disease_clinical_period=cp_cattle,
            disease_immune_period=ip_cattle)
        cattle = ProductionType.objects.all().first()
        DiseaseProgressionAssignment.objects.filter(production_type=cattle).delete()
        DiseaseProgressionAssignment.objects.create(production_type=cattle, progression=disease_progression)

        self.click_navbar_element('Disease Progression')
        self.selenium.find_element_by_partial_link_text('Rename Test').click()
        time.sleep(3)
        self.find('#center-panel').find_element_by_css_selector('select').click()
        time.sleep(1)
        self.find('.edit-button').click()
        time.sleep(1)
        self.find('.overwrite-button').click()

        self.find('#id_equation_type')  # just making sure it's there
        pdf_panel = self.find('#functions_panel')
        pdf_panel.find_element_by_id('id_name').send_keys(' edited')
        time.sleep(1)

        pdf_panel.find_element_by_css_selector('.btn-save').click()
        time.sleep(1)  # there's a reload here
        self.find('#functions_panel .edit-button').click()
        time.sleep(1)  # animate
        self.find('#functions_panel .edit-button-holder .btn-cancel').click()
        time.sleep(1)

        with self.assertRaises(NoSuchElementException):
            self.find('#id_equation_type')  # make sure it's gone

        pdf_updated = ProbabilityFunction.objects.get(pk=lp_cattle.pk)
        self.assertEqual(pdf_updated.name, "Renaming Test - cattle edited")


    @skip("https://github.com/NAVADMC/ADSM/issues/605")
    def test_upload_population_file(self):
        self.click_navbar_element('Population')

        self.selenium.find_element_by_link_text('SampleScenario.sqlite3').click()
        for i in range(5):  # a slow population load
            time.sleep(5) # may need to be adjusted for slow computers or if the file grows
            try:
                self.assertIn('Population File:', self.find('section').text)
                break
            except: pass  # keep trying

    @skip("https://github.com/NAVADMC/ADSM/issues/605")
    def test_upload_blank_population_file(self):
        self.click_navbar_element('Population')

        self.selenium.find_element_by_link_text('blank.sqlite3').click()
        time.sleep(5) # may need to be adjusted for slow computers or if the file grows

        section = self.find('section')
        self.assertIn('Load a Population', section.text)

        alert = self.find('.alert')
        self.assertIn('Error: No Production Types found in the target scenario.', alert.text)

    def test_delete_population(self):
        population = Population.objects.create(source_file="ScenarioCreator/tests/population_fixtures/Population_Test_UTF8.xml")

        self.click_navbar_element('Population', 2)

        # javascript is attaching to this event
        self.find('[data-delete-link]').click()
        time.sleep(2)

        modal = self.selenium.find_element_by_class_name('bootstrap-dialog')

        self.assertIn("Delete Confirmation", modal.text)
        self.assertIn("Are you sure you want to delete the selected Population?", modal.text)

        for button in modal.find_elements_by_tag_name('button'):
            if button.text == "Delete":
                button.click()
                break

        time.sleep(2)

        section = self.find('section')
        self.assertIn('Load a Population', section.text)


    def test_deepest_modal_edit_and_file_upload(self):
        self.setup_scenario()
        self.click_navbar_element("Disease Progression")

        self.selenium.find_element_by_partial_link_text("Cattle Reaction").click()
        # The panel that comes up has id="-setup-DiseaseProgression-1-" when this test is run in isolation, but
        # id="-setup-DiseaseProgression-2-" when the whole series of tests is run. Weird, but we get around it by
        # doing a partial id match using XPath.
        WebDriverWait(self.selenium, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id, '-setup-DiseaseProgression-')]"))
        )
        self.select_option('id_disease_latent_period','Subclinical period - cattle')
        WebDriverWait(self.selenium, timeout=10).until(
            EC.visibility_of_element_located((By.ID, 'functions_panel'))
        )
        self.find('#functions_panel .edit-button').click()
        time.sleep(1)
        self.find('.overwrite-button').click()
        self.select_option('id_equation_type','Histogram')
        time.sleep(1)
        self.select_option('id_graph','Add...')

        time.sleep(1)

        relational_form = self.find('#-setup-RelationalFunction-new-')

        self.assertIn("Import Points from File", relational_form.text)

        #check and see if you can build a Rel from file upload
        relational_form.find_element_by_id("file").send_keys(
            os.path.join(settings.BASE_DIR, "ScenarioCreator","tests","population_fixtures","points.csv"))  # this is sensitive to the starting directory
        relational_form.find_element_by_id('id_name').send_keys('imported from file')
        # Do a "submit" instead of clicking the Apply button. On shorter screens, the Apply button may not be visible,
        # causing the click to fail, and none of the suggested solutions I found for scrolling the button into view
        # worked.
        relational_form.submit()
        time.sleep(3)
        self.select_option('id_graph', 'Add...')
        modal = self.find('div.modal')
        self.assertEqual("123.1", modal.find_element_by_id('id_relationalpoint_set-3-x').get_attribute('value'))


    def test_add_relational_function_by_file(self):
        self.setup_scenario()
        self.click_navbar_element("Zone Effects", 2)
        
        self.find('.addNew a').click()
        WebDriverWait(self.selenium, timeout=10).until(
            EC.presence_of_element_located((By.ID, '-setup-ZoneEffect-new-'))
        )
        self.select_option('id_zone_indirect_movement', 'Add...')
        
        right_panel = self.find('#functions_panel')

        #EDIT click not needed because this is a new form
        # self.find('.edit-button').click()
        # time.sleep(1)
        # self.find('.overwrite-button').click()

        self.submit_relational_form_with_file(right_panel)
        right_panel = self.find('#functions_panel')
        self.assertEqual("123.1", self.find('#id_relationalpoint_set-3-x').get_attribute('value'))


    def submit_relational_form_with_file(self, container):
        container.find_element_by_id("file").send_keys(
            os.path.join(settings.BASE_DIR, "ScenarioCreator","tests","population_fixtures","points.csv"))  # this is sensitive to the starting directory
        container.find_element_by_id('id_name').send_keys('imported from file')
        container.find_element_by_class_name('btn-save').click()
        time.sleep(3)

    def test_pdf_hide_unneeded_fields(self):
        """
            issue 146: unneeded probability fields are not hidden in modals
        """
        self.setup_scenario()
        self.click_navbar_element("Disease Progression")

        target = self.find('.defined_name').click()
        time.sleep(2)

        self.find('#center-panel').find_element_by_css_selector('select').click()
        time.sleep(2)

        right_panel = self.find('#functions_panel')

        mean_field = right_panel.find_element_by_css_selector("#div_id_mean")

        self.assertIn("none", mean_field.value_of_css_property("display"))

    def test_disable_control_master_plan(self):
        self.client.get('/app/OpenTestScenario/ScenarioCreator/tests/population_fixtures/Roundtrip.sqlite3/')
        delete_all_outputs()

        self.click_navbar_element("Controls") 

        parent_of(self.selenium.find_element_by_id("id_disable_all_controls")).click()
        time.sleep(1)

        elements = self.selenium.find_elements_by_css_selector("section > form > div")

        for element in elements:
            el_id = element.get_attribute("id")
            if el_id == "div_id_name" or el_id == "div_id_disable_all_controls":
                self.assertEqual(element.get_attribute("disabled"), None)
            else:
                self.assertEqual(element.get_attribute("disabled"), "true")

        time.sleep(1)
        setup_menu = self.find("#setupMenu")

        hidden_menu_items = [
            "Control Protocol",
            "Protocol Assignments",
            "Zone Effects",
        ]

        for element in setup_menu.find_elements_by_tag_name("a"):
            self.assertNotIn(element.text, hidden_menu_items)


    def test_enable_control_master_plan(self):
        """
            Check that re-enabling the disable all controls option
            in control master plan re-enables the elements and menu
            items
        """
        self.setup_scenario()
        delete_all_outputs()

        ControlMasterPlan.objects.get_or_create(disable_all_controls=True)
        self.click_navbar_element("Controls")
        control_items = [
            "Vaccination Triggers",
            "Control Protocol",
            "Assign Protocols",
            "Zones",
            "Zone Effects"
        ]

        setup_menu = self.selenium.find_element_by_id("setupMenu")
        actual_menu = [x.text for x in setup_menu.find_elements_by_tag_name("a")]
        for controls in control_items:
            self.assertNotIn(controls, actual_menu)

        parent_of(self.selenium.find_element_by_id("id_disable_all_controls")).click()
        time.sleep(1)

        elements = self.selenium.find_elements_by_css_selector("section > form > div")

        for element in elements:
            self.assertEqual(element.get_attribute("disabled"), None)

        setup_menu = self.selenium.find_element_by_id("setupMenu")
        actual_menu = [x.text for x in setup_menu.find_elements_by_tag_name("a")]
        for controls in control_items:
            self.assertIn(controls, actual_menu)

    def test_save_scenario_failure(self):
        filename_field = self.save_scenario_as()
        try:
            filename_field.send_keys('./\\ 123.1&% AZ')
            self.find('.modal.in .btn-primary').click()
            time.sleep(1)

            alert = self.find('.alert-danger')  # this works fine in the actual program.
            
            self.assertIn("Error", alert.text)
        finally:
            try:
                os.remove(workspace_path('Untitled Scenario./\\ 123.1&% AZ.sqlite3'))
            except:
                pass

    def save_scenario_as(self):
        self.cause_unsaved_edit()
        self.find('#TB_file').click()
        time.sleep(1)
        self.find('.current .copy-icon').click()
        time.sleep(1)
        self.find('.btn-dont-save').click()
        time.sleep(1)
        filename_field = self.find('#new_name')
        return filename_field

    def cause_unsaved_edit(self):
        self.find('#id_description').send_keys('--edited--')
        self.find('#submit-id-submit').click()
        time.sleep(1)

    def test_save_scenario_success(self):
        filename_field = self.save_scenario_as()
        try:
            filename_field.send_keys('123.1 AZ')
            self.find('.modal.in .btn-primary').click()
            time.sleep(3)
            status = self.find('.scenario-status')
            self.assertNotIn('unsaved', status.get_attribute('class'))
        finally:
            try:
                os.remove(workspace_path('Untitled Scenario123.1 AZ.sqlite3'))
            except:
                pass

    def use_within_unit_prevalence(self, enable_prevalence, timeout=None):
        """Enables or disables use of within-unit prevalence."""
        if timeout is None:
            timeout = self.default_timeout

        self.click_navbar_element('Disease')
        # Wait for the checkbox to appear
        checkbox = WebDriverWait(self.selenium, timeout=timeout).until(
            EC.visibility_of_element_located((By.NAME, 'use_within_unit_prevalence'))
        )
        # If enable_prevalence==True and the checkbox is not checked, click it to check.
        # If enable_prevalence==False and the checkbox is checked, click it to un-check.
        if enable_prevalence != checkbox.is_selected():
            checkbox.click()

        # Save the changes we just made.
        self.find('.btn-save').click()
        return

    def setup_prevalence_chart(self, disease_progression_name, points, timeout=None):
        """Sets up the prevalence chart for the given Disease Progression."""
        if timeout is None:
            timeout = self.default_timeout

        self.click_navbar_element('Disease Progression')
        # Once the Disease Progression choices come up, click the desired one
        WebDriverWait(self.selenium, timeout=timeout).until(
            EC.visibility_of_element_located((By.LINK_TEXT, disease_progression_name))
        ).click()

        # Once the latent period, etc. choices come up, click to bring up the prevalence chart
        WebDriverWait(self.selenium, timeout=timeout).until(
            EC.visibility_of_element_located((By.ID, 'id_disease_prevalence'))
        ).click()

        # Once the prevalence chart comes up, overwrite the old points with the new ones.
        FunctionsPanel(
            WebDriverWait(self.selenium, timeout=timeout).until(
                EC.visibility_of_element_located((By.ID, 'functions_panel'))
            )
        ).set_points(points)

        return

    def test_overwrite_points_in_relational_function(self):
        """This test checks that the correct number of points are present after overwriting a relational function. See
        the comment "When I went back, I have many rows that must have been saving as I was tinkering around with
        things" in https://github.com/NAVADMC/ADSM/issues/678."""
        self.setup_scenario()

        self.use_within_unit_prevalence(True)
        # Pick the first DiseaseProgression
        disease_progression = DiseaseProgression.objects.all().first()
        points = [(0,0), (1,0.1), (2,0.9), (4,0.2), (10,0)]
        self.setup_prevalence_chart(disease_progression.name, points)

        # Verify that the prevalence chart now has the correct number of points
        current_prevalence_points = RelationalPoint.objects.filter(relational_function=disease_progression.disease_prevalence)
        assert len(current_prevalence_points) == len(points)

    def test_change_one_point_in_relational_function(self):
        """This test checks that the correct number of points are present after editing one point in a relational
         function and that the changed point has the correct value. See https://github.com/NAVADMC/ADSM/issues/678."""
        timeout = self.default_timeout
        self.setup_scenario()

        # Set up a prevalence chart, just like in the test above
        self.use_within_unit_prevalence(True)
        disease_progression = DiseaseProgression.objects.all().first()
        points = [(0,0), (1,0.1), (2,0.9), (4,0.2), (10,0)]
        self.setup_prevalence_chart(disease_progression.name, points)

        # Exit the relational function dialog, then navigate back to it
        self.click_navbar_element('Scenario Description')
        WebDriverWait(self.selenium, timeout=timeout).until(
            EC.visibility_of_element_located((By.ID, 'id_description'))
        )
        self.click_navbar_element('Disease Progression')
        WebDriverWait(self.selenium, timeout=timeout).until(
            EC.visibility_of_element_located((By.LINK_TEXT, disease_progression.name))
        ).click()
        WebDriverWait(self.selenium, timeout=timeout).until(
            EC.visibility_of_element_located((By.ID, 'id_disease_prevalence'))
        ).click()

        # Now reduce the peak from 0.9 to 0.8
        FunctionsPanel(
            WebDriverWait(self.selenium, timeout=timeout).until(
                EC.visibility_of_element_located((By.ID, 'functions_panel'))
            )
        ).change_point(2,(None,0.8))

        # Verify that the chart still has the same number of points
        current_prevalence_points = RelationalPoint.objects.filter(relational_function=disease_progression.disease_prevalence)
        assert len(current_prevalence_points) == len(points)
        # Check that the changed value is what we set it to
        changed_point = current_prevalence_points[2]
        assert abs(changed_point.y - 0.8) < self.tolerance
