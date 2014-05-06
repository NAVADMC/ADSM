from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Percentage(float):
    """This is a type wrapper for float to make it clear if .3 == .3% or 30%.
     This tracks whether the /100 conversion has already been done or not"""
    # def __repr__(self):
    #     return "Percentage(" + super().__repr__() + ")"
    #
    # def __str__(self):
    #     return "Percentage(" + super().__str__() + ")"


class PercentField(models.FloatField, metaclass=models.SubfieldBase):
    """ Float field that ensures field value is in the range 0-100. """
    # default_validators = [
    #     MinValueValidator(0),
    #     MaxValueValidator(100)]

    def to_python(self, value):
        print("to_python", value)
        if type(value) == type(Percentage(50.0)):  # check if it's already converted
            return value
        return Percentage(value / 100)


    def get_db_prep_value(self, value, connection, prepared=False):
        print("get_db_prep_value", value)
        if not value:
            return
        # if not isinstance(value, Percentage):
        #     print( "ValueError: ", value)
        # assert (isinstance(value, Percentage))
        return float(value * 100)  # the type wrapper makes it clear if this has already been converted or not

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
