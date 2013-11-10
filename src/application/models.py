"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class TemperatureReading(ndb.Model):
    """Stored temerature reading"""
    name = ndb.StringProperty(required=True)
    source = ndb.StringProperty(required=True)
    temp_c = ndb.FloatProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)


class TemperatureSetting(ndb.Model):
    """Stored temerature setting"""
    name = ndb.StringProperty(required=True)
    target = ndb.StringProperty(required=True)
    temp_c = ndb.FloatProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
