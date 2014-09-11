import os

from google.appengine.ext import testbed
import webapp2
import webtest

from backend import main
from backend.main import app


ROOT_PATH = os.path.dirname(main.__file__)


class TestCase(object):

    def setUp(self):
        if hasattr(super(TestCase, self), 'setUp'):
            super(TestCase, self).setUp()
        self.configure_appengine()
        self.configure_app()

        # HTTP_HOST is required for any handlers that hit the task queue
        if 'HTTP_HOST' not in os.environ:
            os.environ['HTTP_HOST'] = 'localhost:80'

    def tearDown(self):
        self.testbed.deactivate()

    def configure_appengine(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_mail_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub(root_path=ROOT_PATH)

        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)
        self.taskqueue_stub = self.testbed.get_stub(
            testbed.TASKQUEUE_SERVICE_NAME)
        self.datastore_stub = self.testbed.get_stub(
            testbed.DATASTORE_SERVICE_NAME)

    def configure_app(self):
        app.set_globals(app=app, request=self.get_request())

        if not hasattr(self, 'app'):
            self.app = webtest.TestApp(app)

    @classmethod
    def get_request(cls):
        request = webapp2.Request.blank('/')
        request.app = app
        return request

    @classmethod
    def get_auth(cls):
        return webapp2_extras.auth.get_auth(request=cls.get_request())

    @classmethod
    def get_jinja2(cls):
        return webapp2_extras.jinja2.get_jinja2(app=app)

    @classmethod
    def uri_for(cls, name, *args, **kwargs):
        return webapp2.uri_for(name, cls.get_request(), *args, **kwargs)
