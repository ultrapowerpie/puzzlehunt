import calendar, time, ujson
from flask import Flask, Blueprint, render_template, redirect, \
                  url_for, session, escape, request
from app import db
from util.models import User
from functools import wraps
import os.path

admin = Blueprint('admin', __name__)


################################################################################
#   Rendering templates                                                        #
################################################################################

admin_keys = set(["mypassword"])

capid = "MAXRSVPS".decode("utf8")

rsvped = 1
waitlisted = 2
visited = 3
notvisited = 4

denied = "Sorry, but it looks like you're not on our list."

full = "Oh no! It looks like we've run out of space for this event. The " \
       "puzzle has been solved too many times!"

fresh1 = "Hi "
fresh2 = ", it looks like you're a bit early to the party. Come back next " \
         "year to find out where the puzzle leads!"

greet1 = "Hello "
greet2 = ", we've been expecting you."

def check_solved(func):
    @wraps(func)
    def authenticate(*args, **kwargs):
        if 'solved' not in session:
            return redirect(url_for('admin.index'))
        return func(*args, **kwargs)
    return authenticate


def check_login(func):
    @wraps(func)
    def authenticate(*args, **kwargs):
        if 'netid' not in session:
            return redirect(url_for('admin.index'))
        return func(*args, **kwargs)
    return authenticate


def check_admin(func):
    @wraps(func)
    def authenticate(*args, **kwargs):
        if 'netid' not in session or session['netid'] not in admin_keys:
            return redirect(url_for('admin.index'))
        return func(*args, **kwargs)
    return authenticate

################################################################################
#                                                                              #
#   Administrative Pages                                                       #
#                                                                              #
################################################################################

@admin.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        netid = request.form['email'].split("@")[0]

        if netid in admin_keys:
            session['netid'] = netid
            return redirect(url_for('admin.console'))

        else:
            u = User.query.filter(User.netid == netid).first()
            if not u:
                return render_template("invalid.html", mes=denied)

            if u.member:
                session['netid'] = u.netid
                session['first'] = u.first_name
                return redirect(url_for('admin.countdown'))

            elif u.year == 2019:
                cap = User.query.filter(User.netid == capid).first()
                print User.query.filter(User.rsvp == rsvped).all()
                rsvps = len(User.query.filter(User.rsvp == rsvped).all())

                if rsvps < int(cap.first_name):
                    session['netid'] = u.netid
                    session['first'] = u.first_name
                    u.rsvp = visited
                    db.session.commit()
                    return redirect(url_for('admin.countdown'))

                elif u.rsvp == rsvped:
                    return render_template("invalid.html", mes=full)

                else:
                    u.rsvp = waitlisted
                    db.session.commit()
                    return render_template("invalid.html", mes=full)

            elif u.year == 2020:
                fresh = fresh1+u.first_name+fresh2
                return render_template("invalid.html", mes=fresh)

            else:
                return render_template("invalid.html", mes=denied)

    return render_template("index.html", mes="", hint="")

@admin.route('/countdown', methods=['GET'])
@check_login
def countdown():
    greeting = greet1+session['first']+greet2
    return render_template("countdown.html", mes=greeting)

@admin.route('/rsvp', methods=['POST'])
@check_login
def rsvp():
    checked = request.form['data']
    u = User.query.filter(User.netid == session['netid']).first()

    if u.year != 2019:
        return ujson.dumps({'status':'OK','netid':session['netid'],'rsvp':'0'});

    if checked == "1":
        u.rsvp = rsvped
    else:
        u.rsvp = visited

    db.session.commit()
    return ujson.dumps({'status':'OK','netid':session['netid'],'rsvp':checked});

@admin.route('/console', methods=['GET', 'POST'])
@check_admin
def console():

    cap = User.query.filter(User.netid == capid).first()

    if request.method == 'POST':
        cap.first_name = request.form['cap']
        db.session.commit()

    userlist=User.query.filter(User.year == 2019).all()
    users = []
    rsvp_num = 0
    wait_num = 0
    visit_num = 0
    for u in userlist:
        if int(u.rsvp) == rsvped:
            rsvp_num += 1
            visit_num += 1
        elif int(u.rsvp) == waitlisted:
            wait_num += 1
            visit_num += 1
        elif int(u.rsvp) == visited:
            visit_num += 1
        users.append([u.netid, u.first_name, u.last_name, u.rsvp])

    users = sorted(users, key=lambda x: (x[3], x[1], x[2]))
    for u in users:
        u[0] += "@princeton.edu".decode("utf8")

        status = u[3]

        if status == rsvped:
            message = "RSVP"
        elif status == waitlisted:
            message = "waiting"
        elif status == visited:
            message = "visited"
        else:
            message = "not visited"

        u[3] = message

    return render_template("console.html", cap=cap.first_name,
                            rsvp_num=rsvp_num, wait_num=wait_num,
                            visit_num=visit_num, users=users)
