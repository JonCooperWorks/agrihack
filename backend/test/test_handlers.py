import json

import unittest2

from backend.test import TestCase
from models import Farmer


class ImportHandlerTestCase(TestCase, unittest2.TestCase):

    def test_populate_farmers(self):
        self.assertEqual(0, Farmer.query().count())
        response = self.app.get('/import/')
        self.assertEqual(200, response.status_code)
        self.assertEqual({'status': 'done'}, json.loads(response.body))
        self.assertGreater(Farmer.query().count(), 0)

    def test_farmers_populated_already(self):
        Farmer().put()
        response = self.app.get('/import/')
        self.assertEqual(200, response.status_code)
        self.assertEqual({'status': 'already_populated'}, json.loads(response.body))
        self.assertEqual(1, Farmer.query().count())
