
from FlaskApp import db
from Model import *

# Anything not listed in the second flask import can just be called from the
# imported model
import flask
from flask import Response, render_template,request, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

# This is the application context which does the routing.
app = flask.Flask(__name__)

#################################
# Application routing functions #
@app.route('/')
def main_page():
    """
    Serve the main page from ./templates/main.html
    """
    return render_template("main.html")

@app.route('/characters')
def characters_page():
    """
    Serve the characters list page from ./templates/characters.html
    """
    return render_template("characters.html")
  
@app.route('/characters/<char_id>')
def character_template_page(char_id):
    """
    Serve the character page from ./templates/character_template.html
    """
    return render_template("character_template.html", char_id = char_id)

@app.route('/events')
def events_page():
    """
    Serve the events list page from ./templates/events.html
    """
    return render_template("events.html")
  
@app.route('/events/<event_id>')
def event_template_page(event_id):
    """
    Serve the events list page from ./templates/event_template.html
    """
    return render_template("event_template.html", event_id = event_id)

@app.route('/locations')
def locations_page():
    """
    Serve the locations list page from ./templates/locations.html
    """
    return render_template("locations.html")
  
@app.route('/locations/<loc_id>')
def location_template_page(loc_id):
    """
    Serve the locations list page from ./templates/location_template.html
    """
    return render_template("location_template.html", loc_id = loc_id)

@app.route('/organizations')
def organizations_page():
    """
    Serve the organizations page from ./templates/organizations.html
    """
    return render_template("organizations.html")
  
@app.route('/organizations/<org_id>')
def organization_template_page(org_id):
    """
    Serve the organizations page from ./templates/organization_template.html
    """
    return render_template("organization_template.html", org_id = org_id)

@app.route('/about')
def about_page():
    """
    Serve the about page from ./templates/about.html
    """
    return render_template("about.html")

@app.route('/contact')
def contact_page():
    """
    Serve the contact page from ./templates/contact.html
    """
    return render_template("contact.html")

@app.route('/doc/<path:path>')
def doc_page(path):
    """
    Send documents from the auto-generated html directory.
    
    This implements the documentation routing endpoint.
    """
    return send_from_directory('html',path)

@app.route('/img/<path:path>')
def get_image(path):
    """
    Send files from the ./static/images/ directory, allowing arbitrary linking
    to it from any page.
    
    Use this endpoint instead of embedding url_for('static', ...) in the
    template code.
    """
    return send_from_directory('static/images', path)


@app.route('/api/character')
def get_all_characters():
    return flask.jsonify(Character.query.all())

@app.route('/api/event')
def get_all_events():
    return flask.jsonify(Event.query.all())

@app.route('/api/organization')
def get_all_orgs():
    return flask.jsonify(Organization.query.all())

@app.route('/api/location')
def get_all_locations():
    return flask.jsonify(Location.query.all())

@app.route('/api/membership')
def get_all_memberships():
    return flask.jsonify(Membership.query.all())

@app.route('/tests')
def run_unit_tests():
    return "Hello World"
