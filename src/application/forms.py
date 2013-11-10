"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import TemperatureReading, TemperatureSetting


TemperatureReadingForm = model_form(TemperatureReading, wtf.Form, field_args={
    'name': dict(validators=[validators.Required()]),
    'source': dict(validators=[validators.Required()]),
    'temp_c': dict(validators=[validators.NumberRange(), validators.Required()]),
})


TemperatureSettingForm = model_form(TemperatureSetting, wtf.Form, field_args={
    'name': dict(validators=[validators.Required()]),
    'target': dict(validators=[validators.Required()]),
    'temp_c': dict(validators=[validators.NumberRange(), validators.Required()]),
})
