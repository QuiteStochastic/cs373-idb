
from flask import Flask
from FlaskApp import ConfigTesting, db, drop_all
from flask.ext.sqlalchemy import SQLAlchemy
from unittest import main, TestCase

from Model import Character, Organization, Location, Event

tapp = Flask(__name__)
tdb = db
tapp.config.from_object(ConfigTesting)
tdb.init_app(tapp)

class TestDatabase(TestCase):
    ctx = None
    
    @classmethod
    def setUpClass(cls):
        TestDatabase.ctx = tapp.test_request_context()
        TestDatabase.ctx.push()
        drop_all(tdb)
        tdb.create_all()
        TestDatabase.ctx.pop()
    
    @classmethod
    def tearDownClass(cls):
        TestDatabase.ctx.push()
        drop_all(tdb)
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

def run_tests():
    main()

if __name__ == "__main__":
    run_tests()
