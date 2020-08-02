from chat import db
from chat.models import User, Message
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from chat import common_utills

SUCCESS = 1
FAILURE_USER_EXIST = 2

SENT = 1
RECIEVED = 2


def get_all_messages(username:str, request_flag:int):
    user_id = get_user_id(username)
    messages = Message.query.filter(
        or_(
        Message.sender_id==user_id, 
        Message.receiver_id==user_id
        ))
    
    if request_flag == common_utills.GetAllMessagesFlags.RECEIVED_ONLY:
        messages = messages.filter_by(receiver_id=user_id)
    elif request_flag == common_utills.GetAllMessagesFlags.SENT_ONLY:
        messages = messages.filter_by(sender_id=user_id)
    elif request_flag == common_utills.GetAllMessagesFlags.UNREAD_ONLY:
        print("i'm here)")
        messages = messages.filter_by(receiver_id=user_id, unread_flag=True)
    print("got here")
    
    messages = messages.order_by(db.desc(Message.creation_date)).all()
    for message in messages:
        print(message.unread_flag)
        if message.receiver_id == user_id:
            message.unread_flag = False
    db.session.commit()
    print("got here 2")
    return messages

    
def get_message(sent_or_recieved, username, message_id=None):
    if sent_or_recieved not in [SENT, RECIEVED]:
        raise ValueError("Unexpected value for sent_or_recieved")
    user_id = get_user_id(username)
    
    if message_id:
        return get_message_by_id(user_id, message_id)
        
    if sent_or_recieved == SENT:
        message = Message.query.filter_by(sender_id=user_id).order_by(db.desc(Message.creation_date)).first()
    else:
        message = Message.query.filter_by(receiver_id=user_id).order_by(db.desc(Message.creation_date)).first()
    message.unread_flag = False
    return message
 
def get_message_by_id(user_id, message_id):
    message = Message.query.filter(and_(
        or_(
        Message.sender_id==user_id, 
        Message.receiver_id==user_id
        ),
        Message.id==message_id
        )
        ).order_by(db.desc(Message.creation_date)).first()
    message.unread_flag = False
    return message


def create_user(username:str, hashed_password:str)->int:
    user = User(username=username, password_hash=hashed_password)
    db.session.add(user)
    try: 
        db.session.commit()
    except IntegrityError as e:
        print(e)
        return FAILURE_USER_EXIST
    return SUCCESS

def get_user_id(username:str):
    return User.query.filter_by(username=username).first().id
    