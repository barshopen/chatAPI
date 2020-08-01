from chat.models import db, User, Message
from typing import List, Tuple


def get_all_messages()->List[dict]:
    return [to_dict(message) for message in Message.query.all()]

def get_message(username:str, message_id:int)->dict:
    userid = get_user_id(username)
    if message_id:
        answer = Message.query.filter_by(id=message_id, userid=userid).first()
    else:
        answer = Message.query.filter_by(userid=userid).order_by(db.desc(Message.creation_date)).first()
    return to_dict(answer)


def to_dict(message:Message)->dict:
    return {'subject': message.subject,
    'creation_date': message.creation_date.strftime(r'%m/%d/%y %H:%M:%S'),
    'message': message.message,
    'sender': message.sender.username,
    'receiver': message.receiver.username
    }

def get_user_id(username:str):
    User.query.filter_by(username=username)