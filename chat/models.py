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
    
    def mark_as_read_if_called_from_receiver(self, caller_user:str):
        caller_user_id = get_user_id(caller_user)
        if self.receiver_id == caller_user_id:
            self.unread_flag = False
            db.session.commit()
    
    def __repr__(self):
        return f"Message('{self.subject}')"

class MessageReceivers(db.Model):
    id = db.Column(db.Integer,unique=True, primary_key=True)
    is_sender = (db.Boolean, nullable=False) # sender if is_sender, else receiver

    message_id = db.Column(db.Integer, db.ForeignKey(Message.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    
    message = db.relationship(Message, foreign_keys=[message_id])
    user = db.relationship(User, foreign_keys=[user_id])

class UnreadFlag(db.Model):
    id = db.Column(db.Integer,unique=True, primary_key=True)
    was_read = (db.Boolean, nullable=False, default=False) # indicates whether the message was already read or not (false if unread)

    message_id = db.Column(db.Integer, db.ForeignKey(Message.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    
    message = db.relationship(Message, foreign_keys=[message_id])
    user = db.relationship(User, foreign_keys=[user_id])


def get_user_id(username:str)->int:
    return get_user(username).id

def get_user(username:str)->User:
    return User.query.filter_by(username=username).first()


# some initial data to help me debug
db.drop_all()
db.create_all()
