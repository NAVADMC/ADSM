from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_hooks()
from future.builtins import object
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


