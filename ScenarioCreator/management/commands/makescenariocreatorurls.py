import os
import re

from django.core.management.base import BaseCommand
from django.conf import settings
from django.conf.urls import patterns, url  # do not delete this

from ScenarioCreator.models import *  # do not delete this
from ScenarioCreator.forms import *  # do not delete this


class Command(BaseCommand):
    """Assumes that the only classes in models.py are models.Model.  Because any class will be given a URL,
    whether it is a model or not."""
    @staticmethod
    def generate_urls_from_models(input_file, extra_urls=()):
        assert hasattr(extra_urls, '__getitem__')
        lines = open(input_file, 'r', encoding='utf8').readlines()
        model_strings = extra_urls  # extra_urls is placed first so that they take precedence over auto-urls
        for line in lines:
            if 'class' in line[:5]:
                model_name = re.split('\W+', line)[1]
                model_strings.append("url('^" + model_name + "/$',                      'ScenarioCreator.views.model_list')")
                model_strings.append("url('^" + model_name + "/new/$',                  'ScenarioCreator.views.new_entry')")
                model_strings.append("url('^" + model_name + "/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry')")
                model_strings.append("url('^" + model_name + "/(?P<primary_key>\d+)/copy/$', 'ScenarioCreator.views.copy_entry')")
                model_strings.append("url('^" + model_name + "/(?P<primary_key>\d+)/delete/$', 'ScenarioCreator.views.delete_entry')")

        output = "patterns('', " + ",\n         ".join(model_strings) + ")"
        return output

    def handle(self, *args, **options):
        urls_path = os.path.join(settings.BASE_DIR, 'ScenarioCreator', 'urls.py')
        if os.path.isfile(urls_path):
            os.remove(urls_path)

        urlpatterns = self.generate_urls_from_models(os.path.join(settings.BASE_DIR, 'ScenarioCreator', 'models.py'),
            ["url('^AssignSpreads/$', 'ScenarioCreator.views.assign_disease_spread')",
             "url('^AssignProtocols/$', 'ScenarioCreator.views.assign_protocols')",
             "url('^AssignProgressions/$', 'ScenarioCreator.views.assign_progressions')",
             "url('^AssignZoneEffects/$', 'ScenarioCreator.views.zone_effects')",
             "url('^Protocols.json/$', 'ScenarioCreator.views.protocols_json')",
             "url('^ControlProtocol/$', 'ScenarioCreator.views.control_protocol_list')",
             "url('^ControlProtocol/(?P<primary_key>\d+)/(?P<field>use_\w+)/', 'ScenarioCreator.views.update_protocol_enabled')",

             "url('^Populations/$', 'ScenarioCreator.views.population')",
             "url('^Population/new/$', 'ScenarioCreator.views.population')",  # force redirect for special singleton
             "url('^UploadPopulation/$', 'ScenarioCreator.views.upload_population')",
             "url('^OpenPopulation/(?P<target>.+)$', 'ScenarioCreator.views.open_population')",
             "url('^PopulationPanel/$', 'ScenarioCreator.views.population_panel_only')",  # for async updates

             "url('^ValidateScenario/$', 'ScenarioCreator.views.validate_scenario')",
             "url('^ProductionTypeList.json/$', 'ScenarioCreator.views.production_type_list_json')",
             "url('^PopulationPanelStatus.json/$', 'ScenarioCreator.views.population_panel_status_json')",
             "url('^DisableAllControls.json/$', 'ScenarioCreator.views.disable_all_controls_json')",
             "url('^VaccinationGlobal/$', 'ScenarioCreator.views.vaccination_global')",
             "url('^DestructionGlobal/$', 'ScenarioCreator.views.destruction_global')",

             "url('^ProbabilityDensityFunction/(?P<primary_key>\d+)/graph.png$', 'ScenarioCreator.function_graphs.probability_graph')",
             "url('^RelationalFunction/(?P<primary_key>\d+)/graph.png$', 'ScenarioCreator.function_graphs.relational_graph')",
             "url('^ProbabilityDensityFunction/new/graph.png$', 'ScenarioCreator.function_graphs.empty_graph')",
             "url('^RelationalFunction/new/graph.png$', 'ScenarioCreator.function_graphs.empty_graph')",

             "url('^SpreadOptions.json/$', 'ScenarioCreator.views.spread_options_json')",
             "url('^SpreadInputs.json/$', 'ScenarioCreator.views.spread_inputs_json')",
             "url('^DiseaseSpreadAssignments.json/$', 'ScenarioCreator.views.disease_spread_assignments_json')",
             "url('^ModifySpreadAssignments/$', 'ScenarioCreator.views.modify_spread_assignments')",

             "url('^ExportPopulation/(?P<format>.+)$', 'ScenarioCreator.views.export_population')",
             "url('^ExportFunctions/(?P<block>.+)$', 'ScenarioCreator.views.export_functions')",
             "url('^ImportFunctions/(?P<block>.+)$', 'ScenarioCreator.views.import_functions')",
             "url('^ExportRelGraph/$', 'ScenarioCreator.views.export_relational_graph')",
             "url('^ExportPDFGraph/$', 'ScenarioCreator.views.export_pdf_graph')",
            ])

        urls_code = "\"\"\"URLs is entirely procedural based on the contents of models.py. This has the advantage that urls automatically update as the models change or are renamed.\"\"\"\n\n\n" \
                    "\"\"\"NEVER MODIFY THIS FILE\nInstead, modify the 'makescenariocreatorurls' management command.\"\"\"\n\n" \
                    "from django.conf.urls import patterns, url\n\n" \
                    "urlpatterns = " + urlpatterns

        urls_file = open(urls_path, 'w')
        urls_file.writelines(urls_code)
        urls_file.close()
