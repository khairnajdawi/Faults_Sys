from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Branches
Have name and is_active state to enable or disable login
'''


class Branches(db.Model):
    __tablename__ = 'Branches'

    id = Column(db.Integer, primary_key=True)
    name = Column(String)
    is_active = Column(db.Boolean)

    def __init__(self, name, is_active=True):
        self.name = name
        self.is_active = is_active

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'is_active': self.is_active}
