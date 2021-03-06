import datetime

import unittest2

from backend.test import TestCase
from backend.models import DataPoint, Farmer, Node


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

    def test_get_by_farmer_id(self):
        farmer_key = Farmer(farmer_id='TEST').put()
        farmer = Farmer.get_by_farmer_id('TEST')
        self.assertEqual(farmer_key, farmer.key)

    def test_get_by_cell_number(self):
        farmer_key = Farmer(cell_number='18764243385').put()
        farmer = Farmer.get_by_cell_number('18764243385')
        self.assertEqual(farmer_key, farmer.key)


class NodeTestCase(TestCase, unittest2.TestCase):

    def test_defaults(self):
        node = Node()
        self.assertIsNone(node.node_id)

    def test_get_by_node_id(self):
        node = Node(node_id='TEST').put()
        self.assertEqual(node, Node.get_by_node_id('TEST').key)

    def test_get_data_points(self):
        node = Node()
        node.put()
        for _ in range(10):
            DataPoint(parent=node.key).put()

        self.assertEqual(10, len(node.data_points()))


class DataPointTestCase(TestCase, unittest2.TestCase):

    def test_defaults(self):
        data_point = DataPoint()
        data_point.put()
        self.assertIsNone(data_point.humidity)
        self.assertIsNone(data_point.light)
        self.assertIsNone(data_point.pressure)
        self.assertIsNone(data_point.saturation)
        self.assertIsNone(data_point.temperature)
        self.assertTrue(datetime.datetime.now() -
                        data_point.created < datetime.timedelta(minutes=5))
