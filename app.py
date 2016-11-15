from flask import Flask, Blueprint, session, redirect, url_for, escape, request
from flask_assets import Bundle, Environment
from flask_sqlalchemy import SQLAlchemy
import os, psycopg2

app = Flask(__name__)
wsgi_app = app.wsgi_app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# 'sqlite:///students.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'B4Tr98j/3yD 0pXHe2jmLoL4X//3Qz'
db = SQLAlchemy(app)

from util.assets import *
from views.admin import *

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
