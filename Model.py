from app import db

#################
# Data Modeling #
Participant = db.Table('Participant',
    db.Column('char_id', db.Integer, db.ForeignKey('character.char_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'))
)

Party = db.Table('Party',
    db.Column('org_id', db.Integer, db.ForeignKey('organization.org_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.event_id'))
)

Visitor = db.Table('Visitor',
    db.Column('char_id', db.Integer, db.ForeignKey('character.char_id')),
    db.Column('loc_id', db.Integer, db.ForeignKey('location.loc_id'))
)

class Character(db.Model):
    """
    Models a character from the GoT universe.
    """
    char_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), unique=True)
    last_name = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    religion = db.Column(db.String(255))
    status = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Character('{}')".format(self.name)

class Event(db.Model):
    """
    Models an Event in the GoT universe
    """
    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    event_type = db.Column(db.String(255))
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
    loc_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    loc_type = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('character.char_id'))
    
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
    org_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    org_type = db.Column(db.String(255))
    description = db.Column(db.Text)
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "Organization('{}')".format(self.name)

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
        self.char_id = character.char_id
        self.org_id = orginazation.org_id
        self.rank = rank
        self.active = active
        self.status = "active" if active else "inactive"
    
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
