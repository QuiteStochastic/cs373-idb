
from flask import Flask
from FlaskApp import ConfigTesting, app, db
from flask.ext.sqlalchemy import SQLAlchemy
from unittest import main, TestCase

from Model import Character, Organization, Location, Event

tapp = app
tdb = db

tapp.config.from_object(ConfigTesting)

class TestDatabase(TestCase):
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
        pass
    
    def test_event_double(self):
        pass
    
    def test_event_missing(self):
        pass
    
    def test_org_single(self):
        pass
    
    def test_org_double(self):
        pass
    
    def test_org_missing(self):
        pass
    

def run_tests():
    tdb.create_all()
    Character.query.delete()
    Location.query.delete()
    Organization.query.delete()
    Event.query.delete()
    main()
    tdb.drop_all()

if __name__ == "__main__":
    run_tests()
