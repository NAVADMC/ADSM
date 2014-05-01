from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

__author__ = 'Bryan'


class PercentField(models.FloatField):
    """ Float field that ensures field value is in the range 0-100. """
    default_validators = [
        MinValueValidator(0),
        MaxValueValidator(100)]


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, token=",", *args, **kwargs):
        self.token = token
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value:
            return
        assert (isinstance(value, list))
        return self.token.join([str(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)


from south.modelsinspector import add_introspection_rules

add_introspection_rules([
                            (
                                [ListField],
                                [],
                                {
                                    "token": ["token", {"default": ","}],
                                    },
                            ),
                            ], ["^newline\.modelFields\.ListField"])
