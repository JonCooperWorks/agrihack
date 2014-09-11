import unittest2

from backend.test import TestCase
from backend.models import TestModel


class TestModelTestCase(TestCase, unittest2.TestCase):

    def test_defaults(self):
        t = TestModel()
        self.assertIsNone(t.field)
