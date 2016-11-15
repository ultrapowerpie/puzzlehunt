from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50), unique=False)
    last_name = db.Column(db.String(50), unique=False)
    year = db.Column(db.Integer, unique=False)
    member = db.Column(db.Integer, unique=False)
    rsvp = db.Column(db.Integer, unique=False)

    def __init__(self, netid, first_name, last_name, year, member, rsvp):
        self.netid = netid
        self.first_name = first_name
        self.last_name = last_name
        self.year = year
        self.member = member
        self.rsvp = rsvp

    def __repr__(self):
        return '<User %r>' % (self.netid)
