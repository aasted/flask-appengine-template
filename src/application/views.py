"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
For example the *say_hello* handler, handling the URL route '/hello/<username>',
  must be passed *username* as the argument.

"""
import datetime

from google.appengine.api import memcache, users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import request, render_template, flash, url_for, redirect

from flask_cache import Cache

from application import app
from decorators import login_required, admin_required
from forms import TemperatureReadingBatchForm, TemperatureSettingForm
from models import TemperatureReading, TemperatureReadingBatch, TemperatureSetting


# Flask-Cache (configured to use App Engine Memcache API)
cache = Cache(app)


@login_required
def home():
    """Render the base view"""
    cur_reading = get_current_reading()
    cur_setting = get_current_setting()
    return render_template('home.html', cur_reading=cur_reading, cur_setting=cur_setting)


@login_required
def list_readings():
    """List all temperature readings"""
    readings = TemperatureReadingBatch.query()
    return render_template('list_readings.html', readings=readings)


@login_required
def list_settings():
    """List all temperature readings"""
    settings = TemperatureSetting.query() 
    return render_template('list_settings.html', settings=settings)


@login_required
def reading():
    """Set a batch of readings"""
    form = TemperatureReadingBatchForm()
    if form.validate_on_submit():
        new_reading = TemperatureReadingBatch(
            name=form.name.data,
            source=form.source.data,
            temp_readings_c=form.temp_readings_c.data,
            added_by=users.get_current_user()
        )
        store_batch_reading(new_reading, durable=form.durable.data)
    cur_reading = get_current_reading()
    return render_template('reading.html', cur_reading=cur_reading, form=form)


@login_required
def setting():
    """Fetch or set the current setting"""
    form = TemperatureSettingForm()
    if form.validate_on_submit():
        new_setting = TemperatureSetting(
            name=form.name.data,
            target=form.target.data,
            temp_c=form.temp_c.data,
            added_by=users.get_current_user()
        )
        set_setting(new_setting)
    cur_setting = get_current_setting()
    return render_template('setting.html', cur_setting=cur_setting, form=form)


@admin_required
def admin_only():
    """This view requires an admin account"""
    return 'Super-seekrit admin page.'


def get_current_reading():
    """Return current temperature reading"""
    r = memcache.get('current_reading')
    if r:
        return r.readings()[-1]
    r = TemperatureReadingBatch.query().order(-TemperatureReadingBatch.timestamp).fetch(1)
    if r:
        r = r[0]
        memcache.add('current_reading', r)
        return r.readings()[-1]
    return None


def get_current_setting():
    """Return current temperature setting"""
    r = memcache.get('current_setting')
    if r:
        return r
    r = TemperatureSetting.query().order(-TemperatureSetting.timestamp).fetch(1)
    if r:
        return r[0]
        memcache.add('current_setting', r)
    return r


def store_batch_reading(new_reading, durable):
    """Return True on succesful set, false otherwise"""
    try:
        if durable:
            new_reading.put()
        memcache.set('current_reading', new_reading)
        return True 
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info') 
        return False

def set_setting(new_setting):
    """Return True on succesful set, false otherwise"""
    try:
        new_setting.put()
        memcache.set('current_setting', new_setting)
        return True 
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info') 
        return False


def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''

