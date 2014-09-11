from google.appengine.ext import ndb


class TestModel(ndb.Model):

    field = ndb.StringProperty()


class SMSMessage(ndb.Model):
    body = ndb.StringProperty()
    sender = ndb.StringProperty()

class Node(ndb.Model):
    name = ndb.StringProperty()


class Crop(ndb.Model):
    name = ndb.StringProperty()
    # Ranges



