
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

def run_tests():
    tdb.create_all()
    Character.query.delete()
    main()
    tdb.drop_all()

if __name__ == "__main__":
    run_tests()
