from . import db

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(30))
    age = db.Column(db.Integer)
    occupation = db.Column(db.String(30))
    phone = db.Column(db.Integer())
    alt_phone = db.Column(db.Integer())
    resident = db.Column(db.String(5))
    insurance = db.Column(db.String(5))
    concern = db.Column(db.String(150))
    goal = db.Column(db.String(150))
    past = db.Column(db.String(150))
    #relation = db.relationship('New_User', backref='author', lazy=True)

class New_User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True) #, db.ForeignKey('Client.email'), unique=True)
    name = db.Column(db.String(30))
    uname = db.Column(db.String(30), unique=True)
    password1 = db.Column(db.Integer)
    password2 = db.Column(db.Integer)