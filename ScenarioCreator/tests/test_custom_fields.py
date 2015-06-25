import unittest
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import models
from ScenarioCreator.custom_fields import PercentField


class FieldHolder(models.Model):
    test_field = PercentField()

    class Meta(object):
        abstract = True


class PercentFieldTestCase(TestCase):
    multi_db = True

    def setUp(self):
        self.test_model = FieldHolder()

    def test_valid(self):
        self.test_model.test_field = 0
        self.assertEqual(None, FieldHolder.clean_fields(self.test_model))

        self.test_model.test_field = 1
        self.assertEqual(None, FieldHolder.clean_fields(self.test_model))

        self.test_model.test_field = 0.5
        self.assertEqual(None, FieldHolder.clean_fields(self.test_model))

    def test_invalid_low(self):
        self.test_model.test_field = -1

        with self.assertRaises(ValidationError):
            FieldHolder.clean_fields(self.test_model)

    def test_invalid_high(self):
        self.test_model.test_field = 2

        with self.assertRaises(ValidationError):
            FieldHolder.clean_fields(self.test_model)

    def test_invalid_type(self):
        self.test_model.test_field = "One"

        with self.assertRaises(ValidationError):
            FieldHolder.clean_fields(self.test_model)