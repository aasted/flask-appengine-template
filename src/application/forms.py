"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""
import json

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import TemperatureReadingBatch, TemperatureSetting


def validate_json(form, field):
    """Raise a validationerror if field is not json"""
    try:
        json.loads(field.data)
    except:
        raise wtf.ValidationError("Is not valid json")


class TemperatureReadingBaseForm(wtf.Form):
    durable = wtf.fields.BooleanField('Store durably')


TemperatureReadingBatchForm = model_form(TemperatureReadingBatch, TemperatureReadingBaseForm, field_args={
    'name': dict(validators=[validators.Required()]),
    'source': dict(validators=[validators.Required()]),
    'temp_readings_c': dict(validators=[validators.Required(), validate_json]),
})


TemperatureSettingForm = model_form(TemperatureSetting, wtf.Form, field_args={
    'name': dict(validators=[validators.Required()]),
    'target': dict(validators=[validators.Required()]),
    'temp_c': dict(validators=[validators.NumberRange(), validators.Required()]),
})
