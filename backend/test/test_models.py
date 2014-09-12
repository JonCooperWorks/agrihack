import unittest2

from backend.test import TestCase
from backend.models import Farmer


class FarmerTestCase(TestCase, unittest2.TestCase):

    def test_defaults(self):
        farmer = Farmer()
        self.assertIsNone(farmer.farmer_idx)
        self.assertIsNone(farmer.farmer_id)
        self.assertIsNone(farmer.first_name)
        self.assertIsNone(farmer.last_name)
        self.assertIsNone(farmer.alias)
        self.assertIsNone(farmer.address)
        self.assertIsNone(farmer.parish)
        self.assertIsNone(farmer.cell_number)
        self.assertIsNone(farmer.house_number)
        self.assertFalse(farmer.verified)
        self.assertIsNone(farmer.dob)
        self.assertIsNone(farmer.main_activity)
