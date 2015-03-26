
from FlaskApp import db, app, ConfigTesting
from unittest import main, TestCase

class TestDatabase(TestCase):
    def __init__(self, other):
        db.create_all()
    
    def test_character_single(self):
        pass
    
    def test_character_two(self):
        pass
    
    def test_character_multiple(self):
        pass
    
    def test_org_single(self):
        pass
    
    def test_org_two(self):
        pass
    
    def test_org_multiple(self):
        pass
    
    def test_location_single(self):
        pass
    
    def test_location_two(self):
        pass
    
    def test_location_multiple(self):
        pass
    
    def test_event_single(self):
        pass
    
    def test_event_two(self):
        pass
    
    def test_event_multiple(self):
        pass

if __name__ == "__main__":
    app.config.from_object(ConfigTesting)
    main()
    db.drop_all()
