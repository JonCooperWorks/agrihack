import unittest2

from backend.test import TestCase


class MainHandlerTestCase(TestCase, unittest2.TestCase):

    def test_get(self):
        response = self.app.get('/api/')
        self.assertEqual(200, response.status_code)
        self.assertIn('Agrihack', response.body)
