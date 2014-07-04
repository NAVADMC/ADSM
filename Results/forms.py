from ScenarioCreator.forms import BaseForm
from Results.models import *


class DailyByProductionTypeForm(BaseForm):
    class Meta:
        model = DailyByProductionType


class DailyByZoneForm(BaseForm):
    class Meta:
        model = DailyByZone


class DailyByZoneAndProductionTypeForm(BaseForm):
    class Meta:
        model = DailyByZoneAndProductionType


class DailyControlsForm(BaseForm):
    class Meta:
        model = DailyControls


