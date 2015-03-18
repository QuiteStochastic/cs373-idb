#!/usr/bin/env python3.4

from flask import Flask, Response, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sys
import os.path

#DATABASE = "./house-downing.db"
DEBUG = True
SQLALCHEMY_DATABASE_URI = "postgresql://house-downing.db"
SECRET_KEY = "House Downing Secret Key - xylsi8dh7u19dws4ty63"
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

#################
# Data Modeling #
class Character(db.Model):
    """
    Models a character from the GoT universe.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Character('{}')".format(self.name)

class Event(db.Model):
    """
    Models an Event in the GoT universe
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    
    def __init__(self, name, desc = ""):
        self.name = name
        self.description = desc
    
    def __repr__(self):
        return "Event('{}')".format(self.name)

class Location(db.Model):
    """
    Models a location from the GoT universe.
    """
    ## Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('Organization.id'))
    
    # Relationships
    owner = db.relationship('Character',
                            backref=db.backref('locations', lazy='dynamic'))
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Location('{}')".format(self.name)

class Organization(db.Model):
    """
    Models an organization from the GoT universe.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Organization('{}')".format(self.name)

class User(db.Model):
    """
    A user of this web-service.
    Used for authenticating creation/deletion/updating of data managed by the
    web-service to prevent unauthorized access to those features.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    passwordhash = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    joindate = db.Column(db.Date)
    session = db.Column(db.String(255))
    editor = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    
    def __init__(self, username, password):
        self.username = username
    
    def set_password(self, newpassword):
        """
        Set the users password. This stores the result of hashing the salted
        password in the password_hash member variable.
        """
        self.password_hash = generate_password_hash(newpassword)
    
    def check_password(self, passwd):
        """
        Check the users password (as plain-text) against the stored password
        hash.
        """
        return (self.password_hash == None or
                check_password_hash(self.password_hash, passwd))

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
  
@app.route('/characters/character_template')
def character_template_page():
    """
    Serve the characters list page from ./templates/character_template.html
    """
    return render_template("character_template.html")

@app.route('/events')
def events_page():
    """
    Serve the events list page from ./templates/events.html
    """
    return render_template("events.html")
  
@app.route('/events/event_template')
def event_template_page():
    """
    Serve the events list page from ./templates/event_template.html
    """
    return render_template("event_template.html")

@app.route('/locations')
def locations_page():
    """
    Serve the locations list page from ./templates/locations.html
    """
    return render_template("locations.html")
  
@app.route('/locations/location_template')
def location_template_page():
    """
    Serve the locations list page from ./templates/location_template.html
    """
    return render_template("location_template.html")

@app.route('/organizations')
def organizations_page():
    """
    Serve the organizations page from ./templates/organizations.html
    """
    return render_template("organizations.html")
  
@app.route('/organizations/organization_template')
def organization_template_page():
    """
    Serve the organizations page from ./templates/organization_template.html
    """
    return render_template("organization_template.html")

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

if __name__ == '__main__':
    #app.run(port=8080)
    app.run(host="0.0.0.0", port=8888)
