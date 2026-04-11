from . import db
from datetime import datetime

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    firstName = db.Column(db.String(30))
    lastName = db.Column(db.String(30))
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(30))
    phone = db.Column(db.Integer())
    alt_phone = db.Column(db.Integer())
    resident = db.Column(db.String(5))
    country = db.Column(db.String(45))
    insurance = db.Column(db.String(5))
    reason = db.Column(db.String(150))
    past = db.Column(db.String(150))
    message = db.Column(db.String(150))
    created_at = db.Column(db.DateTime, default=datetime.now())
    users = db.relationship('Users', backref='client', lazy=True)
    notes = db.relationship('Notes', backref='client', lazy=True)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    email = db.Column(db.String(50), unique=True)
    firstName = db.Column(db.String(30))
    lastName = db.Column(db.String(30))
    phone = db.Column(db.Integer())
    created_at = db.Column(db.DateTime, default=datetime.now())

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    email = db.Column(db.String(50))#, unique=True)
    note = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now())
