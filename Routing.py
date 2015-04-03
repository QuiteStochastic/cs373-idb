
from FlaskApp import db, json_response
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
    Serve the event page from ./templates/event_template.html
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
    Serve the location page from ./templates/location_template.html
    """
    return render_template("location_template.html", loc_id = loc_id)

@app.route('/organizations')
def organizations_page():
    """
    Serve the organizations list page from ./templates/organizations.html
    """
    return render_template("organizations.html")
  
@app.route('/organizations/<org_id>')
def organization_template_page(org_id):
    """
    Serve the organization page from ./templates/organization_template.html
    """
    return render_template("organization_template.html", org_id = org_id)
  
@app.route('/episodes')
def episodes_page():
    """
    Serve the episodes list page from ./templates/episodes.html
    """
    return render_template("episodes.html")

@app.route('/episodes/<ep_id>')
def episode_template_page(ep_id):
    """
    Serve the episode page from ./templates/episode_template.html
    """
    return render_template("episode_template.html", ep_id = ep_id)
    

@app.route('/about')
def about_page():
    """
    Serve the about page from ./templates/about.html
    """
    return render_template("about.html")

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

@app.route('/api/characters')
def get_all_characters():
    return json_response([c.serialize() for c in Character.query.all()])

@app.route('/api/characters/<int:cid>')
def get_character(cid):
    ch = Character.query.get(cid)
    if not ch is None:
        return flask.jsonify(ch.serialize())
    return flask.abort(404)

@app.route('/api/events')
def get_all_events():
    return json_response([e.serialize() for e in Event.query.all()])

@app.route('/api/events/<int:eid>')
def get_event(eid):
    event = Event.query.get(eid)
    if event is None:
        flask.abort(404)
    return flask.jsonify(event.serialize())

@app.route('/api/organizations')
def get_all_orgs():
    return json_response([o.serialize() for o in Organization.query.all()])

@app.route('/api/organizations/<int:oid>')
def get_org(oid):
    org = Organization.query.get(oid)
    if org is None:
        flask.abort(404)
    return flask.jsonify(org.serialize())

@app.route('/api/locations')
def get_all_locations():
    return json_response([l.serialize() for l in Location.query.all()])

@app.route('/api/locations/<int:lid>')
def get_location(lid):
    loc = Location.query.get(lid)
    if loc is None:
        flask.abort(404)
    return flask.jsonify(loc.serialize())

@app.route('/api/memberships')
def get_all_memberships():
    return json_response([m.serialize() for m in Membership.query.all()])

@app.route('/api/memberships/<int:mid>')
def get_membership(mid):
    mem = Membership.query.get(mid)
    if mem is None:
        flask.abort(404)
    return flask.jsonify(mem.serialize())

@app.route('/tests')
def run_unit_tests():
    import tests
    return render_template('tests.html', results=tests.test_results_html())
