from google.appengine.ext import ndb


class TestModel(ndb.Model):

    field = ndb.StringProperty()
