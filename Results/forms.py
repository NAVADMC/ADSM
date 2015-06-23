from ScenarioCreator.forms import BaseForm
from Results.models import *


class DailyByProductionTypeForm(BaseForm):
    class Meta(object):
        model = DailyByProductionType
        exclude = []


class DailyByZoneForm(BaseForm):
    class Meta(object):
        model = DailyByZone
        exclude = []


class DailyByZoneAndProductionTypeForm(BaseForm):
    class Meta(object):
        model = DailyByZoneAndProductionType
        exclude = []


class DailyControlsForm(BaseForm):
    class Meta(object):
        model = DailyControls
        exclude = []



