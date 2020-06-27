from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json
import os
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


'''
Branches
Have name and is_active state to enable or disable login
'''


class Branches(db.Model):
    __tablename__ = 'Branches'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String,nullable=False)
    is_active = db.Column(db.Boolean,nullable=False,default=True,server_default='True')
    faults = db.relationship('Faults',backref='faults',cascade='delete,all',lazy=True)

    def __init__(self, name, is_active=True):
        self.name = name
        self.is_active = is_active

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'is_active': self.is_active}


'''
IT Sections
specifiy sections of IT department,
each section has specific faults types responsible for
'''

class ITSections(db.Model):
    __tablename__ = 'ITSections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String,nullable=False)
    is_active = db.Column(db.Boolean,nullable=False,default=True,server_default='True')
    fault_types = db.relationship('FaultTypes',backref='fault_types',cascade='all,delete',lazy=True)

    def __init__(self, name, is_active=True):
        self.name = name
        self.is_active = is_active

    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'is_active': self.is_active}


'''
Fault Types
specifiy faults types and its description, 
also specifiy which it section is responsibile for 
'''


class FaultTypes(db.Model):
    __tablename__ = 'FaultTypes'
    
    id = db.Column(db.Integer, primary_key=True)
    fault_type = db.Column(String,nullable=False)
    it_section = db.Column(db.Integer, db.ForeignKey('ITSections.id',ondelete='cascade'),nullable=False)
    is_active = db.Column(db.Boolean, nullable=False,default=True,server_default='True')

    def __init__(self, fault_type, it_section):
        self.fault_type = fault_type
        self.it_section = it_section

    def format(self):
        return {
          'id': self.id,
          'fault_type': self.fault_type,
          'it_section': self.it_section}


'''
Faults
Faults that get reported by branches to it sections
for fault status, use : 
    1- as new fault, not been seen by it section yet
    2- under progress, fault been seen and the it section in dealing with it
    3- finished, the fault has been fixed
'''

class Faults(db.Model):
    __tablename__ = "Faults"

    id= db.Column(db.Integer,primary_key=True)
    fault_type = db.Column(db.Integer,db.ForeignKey('FaultTypes.id',ondelete='cascade'),nullable=False)
    fault_description = db.Column(db.String,nullable=False)
    branch_id = db.Column(db.Integer,db.ForeignKey('Branches.id',ondelete='cascade'),nullable=False)
    actions = db.relationship('FaultActions',backref='actions',cascade='all,delete',lazy=True)
    status = db.Column(db.Integer,nullable=False,default=1,server_default='1')


'''
Actions
Actions been taken on faults by it sections
will store the action taken, taken by which it section,
the time when the action been done, the current status of
the fault, and the new status 
'''


class FaultActions(db.Model):
    __tablename__ = 'FaultsAction'
    id= db.Column(db.Integer,primary_key=True)
    fault_id = db.Column(db.Integer,db.ForeignKey('Faults.id',ondelete='cascade'),nullable=False)
    action_taken = db.Column(db.String,nullable=False)
    action_by = db.Column(db.Integer,db.ForeignKey('ITSections.id',ondelete='cascade'),nullable=False)
    action_time = db.Column(db.DateTime,nullable=False)
    current_status = db.Column(db.Integer,nullable=False)
    new_status = db.Column(db.Integer,nullable=False)
