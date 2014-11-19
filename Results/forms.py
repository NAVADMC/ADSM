from ScenarioCreator.forms import BaseForm
from Results.models import *


class DailyByProductionTypeForm(BaseForm):
    class Meta(object):
        model = DailyByProductionType


class DailyByZoneForm(BaseForm):
    class Meta(object):
        model = DailyByZone


class DailyByZoneAndProductionTypeForm(BaseForm):
    class Meta(object):
        model = DailyByZoneAndProductionType


class DailyControlsForm(BaseForm):
    class Meta(object):
        model = DailyControls


