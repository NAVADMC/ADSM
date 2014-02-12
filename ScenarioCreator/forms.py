from ScenarioCreator.models import Scenario
from floppyforms import ModelForm

class ScenarioForm(ModelForm):
    class Meta:
        model = Scenario
