from baseapp import db
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

class Rooms(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    yourname = db.Column(db.String(25))
    meetingpwd = db.Column(db.String(25))
    roomname = db.Column(db.String(25))
    roomid = db.Column(db.String(36))
    tmp = db.Column(db.Boolean)

