from google.appengine.ext import ndb


class SMSMessage(ndb.Model):
    body = ndb.StringProperty()
    sender = ndb.StringProperty()


class Farmer(ndb.Model):
    farmer_idx = ndb.IntegerProperty()
    farmer_id = ndb.StringProperty()
    name = ndb.StringProperty()
    alias = ndb.StringProperty()
    address = ndb.StringProperty()
    parish = ndb.StringProperty()
    cell_number = ndb.StringProperty()
    house_number = ndb.StringProperty()
    verified = ndb.BooleanProperty(default=False)
    dob = ndb.DateProperty()
    main_activity = ndb.StringProperty()
    field = ndb.StringProperty()


class Node(ndb.Model):
    name = ndb.StringProperty()


class Crop(ndb.Model):
    name = ndb.StringProperty()
    # Ranges
