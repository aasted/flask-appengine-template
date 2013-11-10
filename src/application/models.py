"""
models.py

App Engine datastore models

"""

import datetime
import json

from google.appengine.ext import ndb


class TemperatureReading(object):
    def __init__(self, name, source, temp_c, timestamp, added_by):
        self.name = name
        self.source = source
        self.temp_c = temp_c
        self.timestamp = timestamp
        self.added_by = added_by


class TemperatureReadingBatch(ndb.Model):
    """Stored temerature reading batch"""
    name = ndb.StringProperty(required=True)
    source = ndb.StringProperty(required=True)
    temp_readings_c = ndb.TextProperty(required=True)  # list of pairs of temp_c, unix timestamp
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

    def readings(self):
        """Return a list of object representations of each temperature reading"""
        return [TemperatureReading(self.name, self.source, temp_c,
                datetime.datetime.fromtimestamp(ts), self.added_by) for(temp_c, ts) in
                json.loads(self.temp_readings_c)]


class TemperatureSetting(ndb.Model):
    """Stored temerature setting"""
    name = ndb.StringProperty(required=True)
    target = ndb.StringProperty(required=True)
    temp_c = ndb.FloatProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
