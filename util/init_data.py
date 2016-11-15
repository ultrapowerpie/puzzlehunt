from app import db
from models import User
import ujson as u

capid = "MAXRSVPS".decode("utf8")
max_num = 100
rsvped = 1
waitlisted = 2
notrsvped = 3
notvisited = 4

def initdb():

    with open("static/data/student_data.json", "rb") as f:
        sd = u.load(f)

    with open("static/data/members.txt", "rb") as f:
        members = set([line.split("@")[0].decode("utf8") for line in f])

    for s in sd:
        netid = s[u'email'].split("@")[0]

        if netid in members:
            usr = User(netid, s[u'first'], s[u'last'], s[u'class'],
                        1, notvisited)
        else:
            usr = User(netid, s[u'first'], s[u'last'],
                        s[u'class'], 0, notvisited)

        db.session.add(usr)

    usr = User(capid, str(max_num).decode("utf8"), "N/A".decode("utf8"),
                3000, 0, 0)
    db.session.add(usr)

    db.session.commit()

    print 'Initialized the database.'
