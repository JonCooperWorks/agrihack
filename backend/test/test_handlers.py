import json

import unittest2

from backend.test import TestCase
from models import DataPoint, Farmer, Node


class ImportHandlerTestCase(TestCase, unittest2.TestCase):

    def test_populate_farmers(self):
        self.assertEqual(0, Farmer.query().count())
        response = self.app.get('/import/')
        self.assertEqual(200, response.status_code)
        self.assertEqual({'status': 'done'}, json.loads(response.body))
        self.assertGreater(Farmer.query().count(), 0)
        self.assertEqual(1, Node.query().count())

    def test_farmers_populated_already(self):
        Farmer().put()
        response = self.app.get('/import/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {'status': 'already_populated'},
            json.loads(response.body))
        self.assertEqual(1, Farmer.query().count())


class DataPointHandlerTestCase(TestCase, unittest2.TestCase):

    def test_add_data_point(self):
        Node(node_id='TEST').put()
        data_point_json = {
            'node_id': 'TEST',
            'temperature': 50,
            'humidity': 40,
            'pressure': 34,
            'light': 14,
            'saturation': 12,
        }
        response = self.app.post_json('/datapoint/', data_point_json)
        self.assertEqual(201, response.status_code)
        self.assertEqual(
            {'status': 'success'},
            json.loads(response.body))
        self.assertEqual(1, DataPoint.query().count())

    def test_add_data_point_invalid_node(self):
        data_point_json = {
            'node_id': 'TEST',
            'temperature': 50,
            'humidity': 40,
            'pressure': 34,
            'light': 14,
            'saturation': 12,
        }
        response = self.app.post_json(
            '/datapoint/',
            data_point_json,
            status=404
        )
        self.assertEqual(404, response.status_code)
