from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from south.modelsinspector import add_introspection_rules


class Percentage(float):
    """This is a type wrapper for float to make it clear if .3 == .3% or 30%.
     This tracks whether the /100 conversion has already been done or not"""
    # def __repr__(self):
    #     return "Percentage(" + super().__repr__() + ")"
    #
    # def __str__(self):
    #     return "Percentage(" + super().__str__() + ")"
    pass


class PercentField(models.FloatField):
    default_validators = [
        MinValueValidator(0.0),
        MaxValueValidator(1.0)]

add_introspection_rules([], ["^ScenarioCreator\.custom_fields\.PercentField"])


class PercentFieldLiteral(models.FloatField):
    """ Currently not used. Float field that ensures field value is in the range 0-100. """
    __metaclass__ = models.SubfieldBase
    default_validators = [
        MinValueValidator(1),
        MaxValueValidator(100)]

    def to_python(self, value):
        print("to_python", value)
        if value >= 1.0:  # check if it's already converted
            return value
        return value * 100

    def get_prep_value(self, value):#, connection, prepared=False):
        print("get_prep_value", value)
        if not value:
            return 0.0
        if value < 1.0:
            return value
        return value / 100

    def value_to_string(self, obj):  # no idea if this has a purpose
        value = self._get_val_from_obj(obj)


class ListField(models.TextField):
    """Written by Bryan Hurst @newline.us"""
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



add_introspection_rules([
                            (
                                [ListField],
                                [],
                                {
                                    "token": ["token", {"default": ","}],
                                    },
                            ),
                            ], ["^newline\.modelFields\.ListField"])
