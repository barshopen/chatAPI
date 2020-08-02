from chat import db
from flask_bcrypt import check_password_hash, generate_password_hash
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def check_password(self, password:str):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"User('{self.username}')"
   
class Message(db.Model):
    id = db.Column(db.Integer,unique=True, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    unread_flag = db.Column(db.Boolean, nullable=False, default=True)
    message = db.Column(db.Text, nullable=False)
    
    sender_id = db.Column(db.Integer, db.ForeignKey(User.id))
    receiver_id = db.Column(db.Integer, db.ForeignKey(User.id))
    
    sender = db.relationship(User, foreign_keys=[sender_id])
    receiver = db.relationship(User, foreign_keys=[receiver_id])

    def __repr__(self):
        return f"Message('{self.subject}')"


db.drop_all()
db.create_all()
a1 = User(username=1, password_hash=generate_password_hash("password"))
db.session.add(a1)
a2 = User(username="ben", password_hash=generate_password_hash("password"))
db.session.add(a2)
a3 = User(username="berry", password_hash=generate_password_hash("password"))
db.session.add(a3)
db.session.commit()
b = Message(subject="hello", creation_date=datetime.datetime.now(), message="hi :)", sender=a1, receiver=a2)
db.session.add(b)
b = Message(subject="hello again!", creation_date=datetime.datetime.now(), message="hi :) :P :)", sender=a1, receiver=a3)
db.session.add(b)
b = Message(subject="hey there!!", creation_date=datetime.datetime.now(), message="hi you yo :)", sender=a2, receiver=a3)
db.session.add(b)
b = Message(subject="hellooooo", creation_date=datetime.datetime.now(), message="hi there :)", sender=a3, receiver=a2)
db.session.add(b)
db.session.commit()