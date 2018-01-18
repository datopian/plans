import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth

from plans.models import UserPlan, Plan
from plans import config


# Create application
app = Flask(__name__, static_folder=None)

app.config['SQLALCHEMY_DATABASE_URI'] = config.database_url
app.config['BASIC_AUTH_USERNAME'] = os.environ['BASIC_AUTH_USERNAME']
app.config['BASIC_AUTH_PASSWORD'] = os.environ['BASIC_AUTH_PASSWORD']
app.config['BASIC_AUTH_FORCE'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.environ['SESSION_SECRET_KEY']

logging.getLogger().setLevel(logging.DEBUG)

db = SQLAlchemy(app)
db.create_all()

admin = Admin(app, url='/plans')
admin.add_view(ModelView(Plan, db.session))
admin.add_view(ModelView(UserPlan, db.session))

basic_auth = BasicAuth(app)

if __name__=='__main__':
    app.run()