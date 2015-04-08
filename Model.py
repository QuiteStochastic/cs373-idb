from FlaskApp import db

#################
# Data Modeling #
Participant = db.Table('participant',
    db.Column('char_id', db.Integer, db.ForeignKey('character.char_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'))
)

Party = db.Table('party',
    db.Column('org_id', db.Integer, db.ForeignKey('organization.org_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'))
)

Visitor = db.Table('visitor',
    db.Column('char_id', db.Integer, db.ForeignKey('character.char_id')),
    db.Column('loc_id', db.Integer, db.ForeignKey('location.loc_id'))
)

class Character(db.Model):
    """
    Models a character from the GoT universe.
    """
    char_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    alias = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    religion = db.Column(db.String(255))
    status = db.Column(db.String(255))
    description = db.Column(db.Text)

    birth_loc = db.Column(db.Integer, db.ForeignKey('location.loc_id'))
    death_loc = db.Column(db.Integer, db.ForeignKey('location.loc_id'))
    first_episode = db.Column(db.Integer, db.ForeignKey('episode.ep_id'))
    last_episode = db.Column(db.Integer, db.ForeignKey('episode.ep_id'))
   
    organization = db.relationship('organization',
                            backref=db.backref('organizations', lazy='dynamic'))
     
    def __init__(self, firstname, lastname):
        db.Model.__init__(self)
        self.first_name = firstname
        self.last_name = lastname
    
    def serialize(self):
        return {
            'char_id':self.char_id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'alias':self.alias,
            'gender':self.gender,
            'religion':self.religion,
            'status':self.status,
            'description':self.description,
            'birth_loc':self.birth_loc,
            'death_loc':self.death_loc,
            'first_episode':self.first_episode,
            'last_episode':self.last_episode
        }
    
    def __repr__(self):
        return "Character('{}', '{}')".format(self.first_name, self.last_name)

class Event(db.Model):
    """
    Models an Event in the GoT universe
    """
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    event_type = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    loc_id = db.Column(db.Integer, db.ForeignKey('location.loc_id'))
    ep_id = db.Column(db.Integer, db.ForeignKey('episode.ep_id'))    
    
    def __init__(self, name, desc = ""):
        db.Model.__init__(self)
        self.name = name
        self.description = desc
    
    def serialize(self):
        return {
            'event_id':self.event_id,
            'name':self.name,
            'event_type':self.event_type,
            'description':self.description,
            'loc_id':self.loc_id,
            'ep_id':self.ep_id
        }
    
    def __repr__(self):
        return "Event('{}')".format(self.name)

class Location(db.Model):
    """
    Models a location from the GoT universe.
    """
    ## Columns
    loc_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    loc_type = db.Column(db.String(255))
    description = db.Column(db.Text)
    superior_loc = db.Column(db.String(255))
    
    # Relationships
    event = db.relationship('episode',
                            backref=db.backref('episodes', lazy='dynamic'))
    chars = db.relationship('character',
                            backref=db.backref('characters', lazy='dynamic'))
    organization = db.relationship('organization',
                            backref=db.backref('organizations', lazy='dynamic'))
 
    def __init__(self, name):
        db.Model.__init__(self)
        self.name = name
    
    def serialize(self):
        return {
            'loc_id':self.loc_id,
            'name':self.name,
            'loc_type':self.loc_type,
            'description':self.description,
            'superior_location':self.superior_loc
        }
    
    def __repr__(self):
        return "Location('{}')".format(self.name)

class Organization(db.Model):
    """
    Models an organization from the GoT universe.
    """
    org_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    org_type = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    loc_id = db.Column(db.Integer, db.ForeignKey('location.loc_id'))
    leader_id = db.Column(db.Integer, db.ForeignKey('character.char_id'))
    
    def __init__(self, name):
        db.Model.__init__(self)
        self.name = name
    
    def serialize(self):
        return {
            'org_id':self.org_id,
            'name':self.name,
            'org_type':self.org_type,
            'description':self.description,
            'loc_id':self.loc_id,
            'leader_id':self.leader_id
        }
    
    def __repr__(self):
        return "Organization('{}')".format(self.name)
      
class Episode(db.Model):
    """
    Models an episode from the GoT series.
    """
    ep_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    season = db.Column(db.Integer)
    episode_number = db.Column(db.Integer)
    description = db.Column(db.Text)

    event = db.relationship('event',
                            backref=db.backref('events', lazy='dynamic'))
    
    def __init__(self, name):
        db.Model.__init__(self)
        self.name = name
    
    def serialize(self):
        return {
            'ep_id':self.ep_id,
            'name':self.name,
            'season':self.season,
            'episode_number':self.episode_number,
            'description':self.description
        }
    
    def __repr__(self):
        return "Episode('{}')".format(self.name)

class Membership(db.Model):
    """
    A characters membership in an organization.
    The many to many relationship between characters and organizations holds
    extra information, hence the need for the extra class.
    """
    member_id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.String(255))
    status = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    
    char_id = db.Column(db.Integer, db.ForeignKey('character.char_id'))
    org_id = db.Column(db.Integer, db.ForeignKey('organization.org_id'))
    
    def __init__(self, character, orginazation, rank, active=True):
        db.Model.__init__(self)
        self.char_id = character.char_id
        self.org_id = orginazation.org_id
        self.rank = rank
        self.active = active
        self.status = "active" if active else "inactive"
    
    def serialize(self):
        return {
            'member_id':self.member_id,
            'rank':self.rank,
            'active':self.active,
            'char_id':self.char_id,
            'org_id':self.org_id
        }
    
    def __repr__(self):
        return "Membership({},{},{},{})".format(self.char_id, self.org_id,
                                                self.rank, self.active)

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
        db.Model.__init__(self)
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
