url('^DbSchemaVersion/new/$', 'ScenarioCreator.views.new_entry'),
url('^DbSchemaVersion/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^DynamicBlob/new/$', 'ScenarioCreator.views.new_entry'),
url('^DynamicBlob/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^DynamicUnit/new/$', 'ScenarioCreator.views.new_entry'),
url('^DynamicUnit/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InChart/new/$', 'ScenarioCreator.views.new_entry'),
url('^InChart/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^ProbabilityEquation/new/$', 'ScenarioCreator.views.new_entry'),
url('^ProbabilityEquation/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^RelationalEquation/new/$', 'ScenarioCreator.views.new_entry'),
url('^RelationalEquation/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^EquationPoint/new/$', 'ScenarioCreator.views.new_entry'),
url('^EquationPoint/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InControlGlobal/new/$', 'ScenarioCreator.views.new_entry'),
url('^InControlGlobal/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InControlPlan/new/$', 'ScenarioCreator.views.new_entry'),
url('^InControlPlan/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InControlsProductionType/new/$', 'ScenarioCreator.views.new_entry'),
url('^InControlsProductionType/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InDiseaseGlobal/new/$', 'ScenarioCreator.views.new_entry'),
url('^InDiseaseGlobal/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InDiseaseProductionType/new/$', 'ScenarioCreator.views.new_entry'),
url('^InDiseaseProductionType/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InDiseaseSpread/new/$', 'ScenarioCreator.views.new_entry'),
url('^InDiseaseSpread/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InGeneral/new/$', 'ScenarioCreator.views.new_entry'),
url('^InGeneral/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InProductionType/new/$', 'ScenarioCreator.views.new_entry'),
url('^InProductionType/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InProductionTypePair/new/$', 'ScenarioCreator.views.new_entry'),
url('^InProductionTypePair/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InZone/new/$', 'ScenarioCreator.views.new_entry'),
url('^InZone/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^InZoneProductionTypePair/new/$', 'ScenarioCreator.views.new_entry'),
url('^InZoneProductionTypePair/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^ReadAllCodes/new/$', 'ScenarioCreator.views.new_entry'),
url('^ReadAllCodes/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),

url('^ReadAllCodeTypes/new/$', 'ScenarioCreator.views.new_entry'),
url('^ReadAllCodeTypes/(?P<primary_key>\d+)/$', 'ScenarioCreator.views.edit_entry'),
