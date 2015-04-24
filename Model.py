from FlaskApp import db
from sqlalchemy.sql import and_, or_, not_

def and_conj(conds):
    r = conds[0]
    for c in conds[1:]:
        r = and_(r, c)
    return r

def or_conj(conds):
    r = conds[0]
    for c in conds[1:]:
        r = or_(r, c)
    return r

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
    
    @classmethod
    def get(cls, charid):
        character = Character.query.get(charid)
        return character if character is not None else Character("","")
    
    @classmethod
    def search(cls, exact, fuzzy, parts):
        name = Character.first_name + ' ' + Character.last_name
        desc = Character.description
        
        c_name_fuzzy = name.ilike(fuzzy)
        c_name_exact = name.ilike(exact)
        c_name_and = and_conj([name.ilike(p) for p in parts])
        c_name_or = or_conj([name.ilike(p) for p in parts])
        
        c_desc_fuzzy = desc.ilike(fuzzy)
        c_desc_and = and_conj([desc.ilike(p) for p in parts])
        c_desc_or = or_conj([desc.ilike(p) for p in parts])
        
        cond = c_name_exact
        name_exact = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(c_name_exact), c_name_fuzzy)
        name_fuzzy = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy])), c_name_and)
        name_and = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and])),
                    c_desc_fuzzy)
        desc_fuzzy = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy])),
                    c_desc_and)
        desc_and = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy, c_desc_and])),
                    c_name_or)
        name_or = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy, c_desc_and, c_name_or])),
                    c_desc_or)
        desc_or = [c.asresult() for c in cls.query.filter(cond).all()]
        
        return (name_exact, name_fuzzy, name_and, desc_fuzzy, desc_and, name_or, desc_or)
    
    def __init__(self, firstname, lastname, desc=None):
        db.Model.__init__(self)
        self.char_id = None
        self.first_name = firstname
        self.last_name = lastname
        self.alias = None
        self.gender = None
        self.religion = None
        self.status = None
        self.description = desc
    
    def serialize(self, brief=False):
        if brief:
            return {
                'char_id':self.char_id,
                'first_name':self.first_name,
                'last_name':self.last_name,
                'status':self.status,
                'religion':self.religion,
                'gender':self.gender
            }
        else:
            return {
                'char_id':self.char_id,
                'first_name':self.first_name,
                'last_name':self.last_name,
                'alias':self.alias,
                'gender':self.gender,
                'religion':self.religion,
                'status':self.status,
                'description':self.description,
                'affiliations':[m.serialize() for m in self.memberships],
                'visited':[l.serialize(True) for l in self.locations],
                'events':[e.serialize(True) for e in self.events]
            }
    
    def asresult(self):
        return {
            "type":"characters",
            "id":self.char_id,
            "name":self.first_name + ' ' + self.last_name,
            "desc":self.description
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
    
    location_id = db.Column(db.Integer, db.ForeignKey('location.loc_id'))
    location = db.relationship("Location", backref="events")
    
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.ep_id'))
    episode = db.relationship("Episode", backref="events")
    
    characters = db.relationship("Character", backref="events",
                                 secondary=Participant)
    organizations = db.relationship("Organization", backref="events",
                                    secondary=Party)
    
    @classmethod
    def get(cls, event_id):
        event = Event.query.get(event_id)
        return event if event is not None else Location("None")
    
    @classmethod
    def search(cls, exact, fuzzy, parts):
        name = Event.name
        desc = Event.description
        
        c_name_fuzzy = name.ilike(fuzzy)
        c_name_exact = name.ilike(exact)
        c_name_and = and_conj([name.ilike(p) for p in parts])
        c_name_or = or_conj([name.ilike(p) for p in parts])
        
        c_desc_fuzzy = desc.ilike(fuzzy)
        c_desc_and = and_conj([desc.ilike(p) for p in parts])
        c_desc_or = or_conj([desc.ilike(p) for p in parts])
        
        cond = c_name_exact
        name_exact = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(c_name_exact), c_name_fuzzy)
        name_fuzzy = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy])), c_name_and)
        name_and = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and])),
                    c_desc_fuzzy)
        desc_fuzzy = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy])),
                    c_desc_and)
        desc_and = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy, c_desc_and])),
                    c_name_or)
        name_or = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy, c_desc_and, c_name_or])),
                    c_desc_or)
        desc_or = [c.asresult() for c in cls.query.filter(cond).all()]
        
        return (name_exact, name_fuzzy, name_and, desc_fuzzy, desc_and, name_or, desc_or)
    
    def __init__(self, name, desc=None, etype=None):
        db.Model.__init__(self)
        self.event_id = None
        self.name = name
        self.event_type = etype
        self.description = desc
        self.location_id = None
        self.episode_id = None
    
    def serialize(self, brief=False):
        if(brief):
            return {
                'event_id':self.event_id,
                'name':self.name
            }
        else:
            return {
                'event_id':self.event_id,
                'name':self.name,
                'event_type':self.event_type,
                'description':self.description,
                'loc_id':self.location_id,
                'loc_name':self.location.name if self.location is not None else "",
                'ep_id':self.episode_id,
                'ep_name':self.episode.name if self.episode is not None else "",
                'participants':[c.serialize(True) for c in self.characters],
                'parties':[o.serialize(True) for o in self.organizations]
            }
    
    def asresult(self):
        return {"type":"events",
                "id":self.event_id,
                "name":self.name,
                "desc":self.description
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
    superior_loc_id = db.Column(db.Integer, db.ForeignKey('location.loc_id'))
    
    superior_loc = db.relationship("Location", uselist=False)
    characters = db.relationship("Character", backref="locations",
                                 secondary=Visitor)
    
    @classmethod
    def get(cls, locid):
        location = Location.query.get(locid)
        return location if location is not None else Location("")
    
    @classmethod
    def search(cls, exact, fuzzy, parts):
        name = Location.name
        desc = Location.description
        
        c_name_fuzzy = name.ilike(fuzzy)
        c_name_exact = name.ilike(exact)
        c_name_and = and_conj([name.ilike(p) for p in parts])
        c_name_or = or_conj([name.ilike(p) for p in parts])
        
        c_desc_fuzzy = desc.ilike(fuzzy)
        c_desc_and = and_conj([desc.ilike(p) for p in parts])
        c_desc_or = or_conj([desc.ilike(p) for p in parts])
        
        cond = c_name_exact
        name_exact = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(c_name_exact), c_name_fuzzy)
        name_fuzzy = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy])), c_name_and)
        name_and = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and])),
                    c_desc_fuzzy)
        desc_fuzzy = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy])),
                    c_desc_and)
        desc_and = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy, c_desc_and])),
                    c_name_or)
        name_or = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy, c_desc_and, c_name_or])),
                    c_desc_or)
        desc_or = [c.asresult() for c in cls.query.filter(cond).all()]
        
        return (name_exact, name_fuzzy, name_and, desc_fuzzy, desc_and, name_or, desc_or)
    
    def __init__(self, name, desc=None, ltype=0):
        db.Model.__init__(self)
        self.loc_id = None
        self.name = name
        self.loc_type = ltype
        self.description = desc
        self.superior_loc_id = None
    
    def serialize(self, brief=False):
        if brief:
            return {
                'loc_id':self.loc_id,
                'name':self.name,
                'loc_type':self.loc_type,
                'superior_location':self.superior_loc.name if self.superior_location is not None else ""
            }
        else:
            return {
                'loc_id':self.loc_id,
                'name':self.name,
                'loc_type':self.loc_type,
                'description':self.description,
                'superior_location':self.superior_loc.name if self.superior_loc is not None else "",
                'visitors':[c.serialize(True) for c in self.characters],
                'events':[e.serialize(True) for e in self.events],
                'organizations':[o.serialize(True) for o in self.organizations]
            }
    
    def asresult(self):
        return {"type":"locations",
                "id":self.loc_id,
                "name":self.name,
                "desc":self.description
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
    
    location_id = db.Column(db.Integer, db.ForeignKey('location.loc_id'))
    location = db.relationship("Location", backref="organizations")
    leader_id = db.Column(db.Integer, db.ForeignKey('character.char_id'))
    leader = db.relationship("Character", backref="leader")
    
    @classmethod
    def get(cls, orgid):
        org = Organization.query.get(orgid)
        return org if org is not None else Organization("")
    
    @classmethod
    def search(cls, exact, fuzzy, parts):
        name = Organization.name
        desc = Organization.description
        
        c_name_fuzzy = name.ilike(fuzzy)
        c_name_exact = name.ilike(exact)
        c_name_and = and_conj([name.ilike(p) for p in parts])
        c_name_or = or_conj([name.ilike(p) for p in parts])
        
        c_desc_fuzzy = desc.ilike(fuzzy)
        c_desc_and = and_conj([desc.ilike(p) for p in parts])
        c_desc_or = or_conj([desc.ilike(p) for p in parts])
        
        cond = c_name_exact
        name_exact = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(c_name_exact), c_name_fuzzy)
        name_fuzzy = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy])), c_name_and)
        name_and = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and])),
                    c_desc_fuzzy)
        desc_fuzzy = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy])),
                    c_desc_and)
        desc_and = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy, c_desc_and])),
                    c_name_or)
        name_or = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy, c_desc_and, c_name_or])),
                    c_desc_or)
        desc_or = [c.asresult() for c in cls.query.filter(cond).all()]
        
        return (name_exact, name_fuzzy, name_and, desc_fuzzy, desc_and, name_or, desc_or)
    
    def __init__(self, name, desc=None, org_type=0):
        db.Model.__init__(self)
        self.org_id = None
        self.name = name
        self.org_type = None
        self.description = desc
        self.location_id = None
        self.leader_id = None
    
    def serialize(self, brief=False):
        if brief:
            return {
                'org_id':self.org_id,
                'name':self.name,
                'org_type':self.org_type
            }
        else:
            return {
                'org_id':self.org_id,
                'name':self.name,
                'org_type':self.org_type,
                'description':self.description,
                'location_id':self.location_id,
                'location_name':self.location.name if self.location is not None else "",
                'leader_id':self.leader_id,
                'leader_first_name':self.leader.first_name if self.leader is not None else "",
                'leader_last_name':self.leader.last_name if self.leader is not None else "",
                'members':[m.serialize() for m in self.members],
                'partyto':[e.serialize(True) for e in self.events]
            }
    
    def asresult(self):
        return {"type":"organizations",
                "id":self.org_id,
                "name":self.name,
                "desc":self.description
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
    
    @classmethod
    def search(cls, exact, fuzzy, parts):
        name = Episode.name
        desc = Episode.description
        
        c_name_fuzzy = name.ilike(fuzzy)
        c_name_exact = name.ilike(exact)
        c_name_and = and_conj([name.ilike(p) for p in parts])
        c_name_or = or_conj([name.ilike(p) for p in parts])
        
        c_desc_fuzzy = desc.ilike(fuzzy)
        c_desc_and = and_conj([desc.ilike(p) for p in parts])
        c_desc_or = or_conj([desc.ilike(p) for p in parts])
        
        cond = c_name_exact
        name_exact = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(c_name_exact), c_name_fuzzy)
        name_fuzzy = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy])), c_name_and)
        name_and = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and])),
                    c_desc_fuzzy)
        desc_fuzzy = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy])),
                    c_desc_and)
        desc_and = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy, c_desc_and])),
                    c_name_or)
        name_or = [c.asresult() for c in cls.query.filter(cond).all()]
        
        cond = and_(not_(or_conj([c_name_exact, c_name_fuzzy, c_name_and,
                                  c_desc_fuzzy, c_desc_and, c_name_or])),
                    c_desc_or)
        desc_or = [c.asresult() for c in cls.query.filter(cond).all()]
        
        return (name_exact, name_fuzzy, name_and, desc_fuzzy, desc_and, name_or, desc_or)
    
    def __init__(self, name, desc=None):
        db.Model.__init__(self)
        self.ep_id = None
        self.name = name
        self.season = None
        self.episode_number = None
        self.description = desc
    
    def serialize(self, brief=False):
        if brief:
            return {
                'ep_id':self.ep_id,
                'name':self.name,
                'season':self.season,
                'episode_number':self.episode_number
            }
        else:
            return {
                'ep_id':self.ep_id,
                'name':self.name,
                'season':self.season,
                'episode_number':self.episode_number,
                'description':self.description,
                'events':[e.serialize() for e in self.events]
            }
    
    def asresult(self):
        return {
            "type":"episodes",
            "id":self.ep_id,
            "name":self.name,
            "desc":self.description
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
    
    character_id = db.Column(db.Integer, db.ForeignKey('character.char_id'))
    character = db.relationship("Character", backref="memberships")
    org_id = db.Column(db.Integer, db.ForeignKey('organization.org_id'))
    org = db.relationship("Organization", backref="members")
    
    def __init__(self, character, orginazation, rank, active=True):
        db.Model.__init__(self)
        self.character_id = character.char_id
        self.org_id = orginazation.org_id
        self.rank = rank
        self.active = active
        self.status = "active" if active else "inactive"
    
    def serialize(self):
        return {
            'member_id':self.member_id,
            'rank':self.rank,
            'active':self.active,
            'char_id':self.character_id,
            'char_first_name':self.character.first_name if self.character is not None else "", 
            'char_last_name':self.character.last_name if self.character is not None else "",
            'org_id':self.org_id,
            'org_name':self.org.name if self.org is not None else ""
        }
    
    def __repr__(self):
        return "Membership({},{},{},{})".format(self.char_id, self.org_id,
                                                self.rank, self.active)

# A list of things we want to remove from the string
_default_matches = ["@", "-", ".", "!", "?", ",", "<", ">", '"', "'", "=", "_"]
def search_sanitize(s, match = None):
    if match is None:
        match = _default_matches
    
    for m in match:
        s.replace(m, ' ')
    return s

def search_combine(*results):
    rlist = []
    # Combine by ordering
    for r in results:
        if len(rlist) < len(r):
            rlist.extend([[] for i in range(len(r) - len(rlist))])
        for i, l in enumerate(r):
            rlist[i].extend(l)
    
    # Combine all
    flist = []
    for l in rlist:
        flist.extend(l)
    
    return flist

def searchdb(searchterm):
    """
    Search the models for matches to searchterm.
    """
    # name exact, description exact, name and, description and, name or,
    # descrption or
    exact = '%'+search_sanitize(searchterm)+'%'
    parts = ['%'+s+'%' for s in search_sanitize(searchterm).split()]
    results = search_combine(Character.search(searchterm, exact, parts),
                             Episode.search(searchterm, exact, parts),
                             Event.search(searchterm, exact, parts),
                             Location.search(searchterm, exact, parts),
                             Organization.search(searchterm, exact, parts))
    return {"searchterm":searchterm,
            "resultCount":len(results),
            "results":results}
