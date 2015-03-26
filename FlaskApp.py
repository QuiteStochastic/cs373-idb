
from flask import Flask, Response, render_template,request
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class ConfigBase(object):
    DEBUG = True
    SECRET_KEY = "House Downing Secret Key - xylsi8dh7u19dws4ty63"
    USERNAME = 'webapp'
    PASSWORD = 'gotswe'

class ConfigProduction(ConfigBase):
    SQLALCHEMY_DATABASE_URI = "postgresql://webapp:gotswe@127.0.0.1/housedowning"

class ConfigRemote(ConfigBase):
    SQLALCHEMY_DATABASE_URI = "postgresql://webapp:gotswe@104.130.247.236/housedowning"

class ConfigTesting(ConfigBase):
    SQLALCHEMY_DATABASE_URI = "postgresql://webapp:gotswe@104.130.247.236/HouseDowningTesting"

app = Flask(__name__)
db = SQLAlchemy(app)

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
