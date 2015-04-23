
from app import running
from flask import Flask
from FlaskApp import ConfigTesting, db, drop_all
from Routing import app
from flask.ext.sqlalchemy import SQLAlchemy
from unittest import main, TestCase, TextTestRunner
from io import StringIO
import json

from Model import *

tapp = Flask(__name__)
tdb = db

standalone = False

class TestApi(TestCase):
    ctx = None
    
    @classmethod
    def setUpClass(cls):
        TestApi.ctx = app.test_request_context()
        #tdb.init_app(app)
        app.debug = True
        if standalone:
            TestApi.ctx.push()
            tdb.create_all()
            # Create data
            tdb.session.add(Character('Robert', 'Baratheon'))
            tdb.session.add(Event('Battle of Blackwater Bay'))
            tdb.session.add(Location('Kings Landing'))
            tdb.session.add(Organization('House Stark'))
            tdb.session.add(Episode('Episode 1'))
            
            tdb.session.commit()
            TestApi.ctx.pop()
    
    @classmethod
    def tearDownClass(cls):
        TestApi.ctx = None
    
    def setUp(self):
        """
        Make the request context current
        """
        TestApi.ctx.push()
    
    def tearDown(self):
        """
        Remove the test context from the stack
        """
        TestApi.ctx.pop()
    
    ###################################
    # Character Tests (/api/characters)
    def test_api_character_list_response(self):
        client = app.test_client()
        response = client.get('/api/characters')
        self.assertEqual(response.status_code, 200)
    
    def test_api_character_list_count(self):
        client = app.test_client()
        response = client.get('/api/characters')
        objects = json.loads(response.data.decode("utf-8"))
        self.assertTrue(len(objects) > 0)
    
    def test_api_character_list_type(self):
        client = app.test_client()
        response = client.get('/api/characters')
        objects = json.loads(response.data.decode("utf-8"))
        self.assertTrue(type(objects) == list)
    
    ######################################
    # Character Tests (/api/characters/id)
    def test_api_character_individual_response(self):
        client = app.test_client()
        response = client.get('/api/characters/1')
        self.assertEqual(response.status_code, 200)
    
    def test_api_character_individual_valid(self):
        client = app.test_client()
        response = client.get('/api/characters/1')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.data.decode("utf-8"))
        self.assertTrue(type(obj) == dict)
        self.assertEqual(obj["char_id"], 1)
    
    def test_api_character_individual_invalid(self):
        client = app.test_client()
        response = client.get('/api/characters/99999999')
        self.assertEqual(response.status_code, 404)
    
    ##################################
    # Episode Tests (/api/episodes/id)
    def test_api_episode_list_response(self):
        client = app.test_client()
        response = client.get('/api/episodes')
        self.assertEqual(response.status_code, 200)
    
    def test_api_episode_list_count(self):
        client = app.test_client()
        response = client.get('/api/episodes')
        objects = json.loads(response.data.decode("utf-8"))
        self.assertTrue(len(objects) > 0)
    
    def test_api_episode_list_type(self):
        client = app.test_client()
        response = client.get('/api/episodes')
        objects = json.loads(response.data.decode("utf-8"))
        self.assertTrue(type(objects) == list)
    
    ##################################
    # Episode Tests (/api/episodes/id)
    def test_api_episode_individual_response(self):
        client = app.test_client()
        response = client.get('/api/episodes/1')
        self.assertEqual(response.status_code, 200)
    
    def test_api_episode_individual_valid(self):
        client = app.test_client()
        response = client.get('/api/episodes/1')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.data.decode("utf-8"))
        self.assertTrue(type(obj) == dict)
        self.assertEqual(obj["ep_id"], 1)
    
    def test_api_episode_individual_invalid(self):
        client = app.test_client()
        response = client.get('/api/episodes/99999999')
        self.assertEqual(response.status_code, 404)
    
    ###########################
    # Event Tests (/api/events)
    def test_api_event_list_response(self):
        client = app.test_client()
        response = client.get('/api/events')
        self.assertEqual(response.status_code, 200)
    
    def test_api_event_list_count(self):
        client = app.test_client()
        response = client.get('/api/events')
        objects = json.loads(response.data.decode("utf-8"))
        self.assertTrue(len(objects) > 0)
    
    def test_api_event_list_type(self):
        client = app.test_client()
        response = client.get('/api/events')
        objects = json.loads(response.data.decode("utf-8"))
        self.assertTrue(type(objects) == list)
    
    ##############################
    # Event Tests (/api/events/id)
    def test_api_event_individual_response(self):
        client = app.test_client()
        response = client.get('/api/events/1')
        self.assertEqual(response.status_code, 200)
    
    def test_api_event_individual_valid(self):
        client = app.test_client()
        response = client.get('/api/events/1')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.data.decode("utf-8"))
        self.assertTrue(type(obj) == dict)
        self.assertEqual(obj["event_id"], 1)
    
    def test_api_event_individual_invalid(self):
        client = app.test_client()
        response = client.get('/api/events/99999999')
        self.assertEqual(response.status_code, 404)
    
    ###########################
    # Location Tests (/api/locations)
    def test_api_location_list_response(self):
        client = app.test_client()
        response = client.get('/api/locations')
        self.assertEqual(response.status_code, 200)
    
    def test_api_location_list_count(self):
        client = app.test_client()
        response = client.get('/api/locations')
        objects = json.loads(response.data.decode("utf-8"))
        self.assertTrue(len(objects) > 0)
    
    def test_api_location_list_type(self):
        client = app.test_client()
        response = client.get('/api/locations')
        objects = json.loads(response.data.decode("utf-8"))
        self.assertTrue(type(objects) == list)
    
    ##############################
    # Location Tests (/api/locations/id)
    def test_api_location_individual_response(self):
        client = app.test_client()
        response = client.get('/api/locations/1')
        self.assertEqual(response.status_code, 200)
    
    def test_api_location_individual_valid(self):
        client = app.test_client()
        response = client.get('/api/locations/1')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.data.decode("utf-8"))
        self.assertTrue(type(obj) == dict)
        self.assertEqual(obj["loc_id"], 1)
    
    def test_api_location_individual_invalid(self):
        client = app.test_client()
        response = client.get('/api/locations/99999999')
        self.assertEqual(response.status_code, 404)
    
    ###########################
    # Organization Tests (/api/organizations)
    def test_api_organization_list_response(self):
        client = app.test_client()
        response = client.get('/api/organizations')
        self.assertEqual(response.status_code, 200)
    
    def test_api_organization_list_count(self):
        client = app.test_client()
        response = client.get('/api/organizations')
        objects = json.loads(response.data.decode("utf-8"))
        self.assertTrue(len(objects) > 0)
    
    def test_api_organization_list_type(self):
        client = app.test_client()
        response = client.get('/api/organizations')
        objects = json.loads(response.data.decode("utf-8"))
        self.assertTrue(type(objects) == list)
    
    ##############################
    # Organization Tests (/api/organizations/id)
    def test_api_organization_individual_response(self):
        client = app.test_client()
        response = client.get('/api/organizations/1')
        self.assertEqual(response.status_code, 200)
    
    def test_api_organization_individual_valid(self):
        client = app.test_client()
        response = client.get('/api/organizations/1')
        self.assertEqual(response.status_code, 200)
        obj = json.loads(response.data.decode("utf-8"))
        self.assertTrue(type(obj) == dict)
        self.assertEqual(obj["org_id"], 1)
    
    def test_api_organization_individual_invalid(self):
        client = app.test_client()
        response = client.get('/api/organizations/99999999')
        self.assertEqual(response.status_code, 404)

class TestDatabase(TestCase):
    ctx = None
    
    @classmethod
    def setUpClass(cls):
        TestDatabase.ctx = tapp.test_request_context()
        TestDatabase.ctx.push()
        tdb.drop_all()
        tdb.create_all()
        TestDatabase.ctx.pop()
    
    @classmethod
    def tearDownClass(cls):
        TestDatabase.ctx.push()
        tdb.drop_all()
        TestDatabase.ctx.pop()
    
    def setUp(self):
        """
        Make the request context current
        """
        TestDatabase.ctx.push()
    
    def tearDown(self):
        """
        Remove the test context from the stack
        """
        TestDatabase.ctx.pop()
    
    def test_character_single(self):
        c1 = Character("Robert", "Baratheon")
        tdb.session.add(c1)
        tdb.session.commit()
        
        c2 = Character.query.filter_by(first_name="Robert").first()
        self.assertEqual(c2.first_name, c1.first_name)
        
    def test_character_double(self):
        c1 = Character("Jeofery", "Baratheon")
        c2 = Character("Eddard", "Stark")
        tdb.session.add(c1)
        tdb.session.add(c2)
        tdb.session.commit()
        
        c3 = Character.query.filter_by(char_id=c1.char_id).first()
        self.assertEqual(c3.first_name, c1.first_name)
        c4 = Character.query.filter_by(first_name="Eddard").first()
        self.assertEqual(c4.first_name, c2.first_name)
        
    def test_character_missing(self):
        c1 = Character.query.filter_by(first_name="Obama").first()
        self.assertTrue(c1 is None)
        
    def test_location_single(self):
        l1 = Location("Blackwater Bay")
        tdb.session.add(l1)
        tdb.session.commit()
        
        l2 = Location.query.filter_by(name="Blackwater Bay").first()
        self.assertEqual(l2.loc_id, l1.loc_id)
        
    def test_location_double(self):
        c1 = Location("Kings Landing")
        c2 = Location("Winterfell")
        tdb.session.add(c1)
        tdb.session.add(c2)
        tdb.session.commit()
        
        c3 = Location.query.filter_by(loc_id=c1.loc_id).first()
        self.assertEqual(c3.name, c1.name)
        c4 = Location.query.filter_by(name="Winterfell").first()
        self.assertEqual(c4.loc_id, c2.loc_id)
        
    def test_location_missing(self):
        c1 = Location.query.filter_by(name="University of Texas").first()
        self.assertTrue(c1 is None)
        
    def test_event_single(self):
        l1 = Event("The Red Wedding", "People gunna die")
        tdb.session.add(l1)
        tdb.session.commit()
        
        l2 = Event.query.filter_by(name="The Red Wedding").first()
        self.assertEqual(l2.event_id, l1.event_id)
        
    def test_event_double(self):
        c1 = Event("The Beheading of Ned Stark")
        c2 = Event("Battle of Blackwater Bay")
        tdb.session.add(c1)
        tdb.session.add(c2)
        tdb.session.commit()
        
        c3 = Event.query.filter_by(event_id=c1.event_id).first()
        self.assertEqual(c3.name, c1.name)
        c4 = Event.query.filter_by(name="Battle of Blackwater Bay").first()
        self.assertEqual(c4.event_id, c2.event_id)
        
    def test_event_missing(self):
        c1 = Event.query.filter_by(name="The Grading of This Project").first()
        self.assertTrue(c1 is None)
        
    def test_org_single(self):
        l1 = Organization("The Nights Watch")
        tdb.session.add(l1)
        tdb.session.commit()
        
        l2 = Organization.query.filter_by(name="The Nights Watch").first()
        self.assertEqual(l2.org_id, l1.org_id)
        
    def test_org_double(self):
        c1 = Organization("White Walkers")
        c2 = Organization("House Arryn")
        tdb.session.add(c1)
        tdb.session.add(c2)
        tdb.session.commit()
        
        c3 = Organization.query.filter_by(org_id=c1.org_id).first()
        self.assertEqual(c3.name, c1.name)
        c4 = Organization.query.filter_by(name="House Arryn").first()
        self.assertEqual(c4.org_id, c2.org_id)
        
    def test_org_missing(self):
        c1 = Organization.query.filter_by(name="House Downing").first()
        self.assertTrue(c1 is None)

def test_results_html():
    return run_tests().split('\n')

def run_tests():
    import sys
    
    s = StringIO()
    runner = TextTestRunner(s, verbosity=2)
    sys.argv = [sys.argv[0]]
    
    tapp.config.from_object(ConfigTesting)
    tdb.init_app(tapp)
    
    main(module=__name__, testRunner=runner, exit=False)
    return s.getvalue()

if __name__ == "__main__":
    # If we are running it by itself, we need to init the app object
    standalone = True
    tdb.init_app(app)
    app.config.from_object(ConfigTesting)
    # We also need to import the routing information
    print(run_tests())
