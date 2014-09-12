from google.appengine.ext import ndb


class SMSMessage(ndb.Model):
    body = ndb.StringProperty()
    sender = ndb.StringProperty()


class Farmer(ndb.Model):
    farmer_idx = ndb.IntegerProperty()
    farmer_id = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    alias = ndb.StringProperty()
    address = ndb.StringProperty()
    parish = ndb.StringProperty()
    cell_number = ndb.StringProperty()
    house_number = ndb.StringProperty()
    verified = ndb.BooleanProperty(default=False)
    dob = ndb.DateProperty()
    main_activity = ndb.StringProperty()
    field = ndb.StringProperty()

    @classmethod
    def get_by_farmer_id(cls, farmer_id):
        return cls.query().filter(cls.farmer_id == farmer_id).get()


class Node(ndb.Model):
    node_id = ndb.StringProperty()

    @classmethod
    def get_by_node_id(cls, node_id):
        return cls.query().filter(cls.node_id == node_id).get()

    def data_points(self):
        return DataPoint.query(ancestor=self.key).fetch()


class DataPoint(ndb.Model):
    temperature = ndb.IntegerProperty()
    pressure = ndb.IntegerProperty()
    humidity = ndb.IntegerProperty()
    light = ndb.IntegerProperty()
    saturation = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)


class Crop(ndb.Model):
    name = ndb.StringProperty()
    # Ranges
