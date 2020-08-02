from chat import db, models
from chat.models import User, Message, get_user, get_user_id
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from chat import common_utills


SENT = 1
RECIEVED = 2



def delete_message(username:str, message_id:int)->int:
    user_id = get_user_id(username)

    message = get_message_by_id(user_id, message_id)
    
    if not message:
        return common_utills.DeleteMessageStatusCodes.MESSAGE_DOES_NOT_EXIST
    Message.query.filter(Message.id == message.id).delete()
    db.session.commit()
    
    message = get_message_by_id(username, message_id)
    if message:
        return common_utills.DeleteMessageStatusCodes.DELETE_FAILED
    return common_utills.DeleteMessageStatusCodes.DELETE_SUCCESSFUL

    
def write_message(sender_username:str, receiver_username:str, subject:str, message:str)->Message:
    message = Message(subject=subject, 
                      message=message, 
                      sender=get_user(sender_username), 
                      receiver=get_user(receiver_username)
                      )
    db.session.add(message)
    db.session.commit()
    
    return message
    
    
def get_all_messages(username:str, request_flag:int):
    user_id = get_user_id(username)
    messages = Message.query.filter(
        or_(
        Message.sender_id==user_id, 
        Message.receiver_id==user_id
        ))
    
    if request_flag == common_utills.GetAllMessagesStatusCodes.RECEIVED_ONLY:
        messages = messages.filter_by(receiver_id=user_id)
    elif request_flag == common_utills.GetAllMessagesStatusCodes.SENT_ONLY:
        messages = messages.filter_by(sender_id=user_id)
    elif request_flag == common_utills.GetAllMessagesStatusCodes.UNREAD_ONLY:
        messages = messages.filter_by(receiver_id=user_id, unread_flag=True)
    
    messages = messages.order_by(db.desc(Message.creation_date))
    db.session.commit()
    return messages.all()
    
def get_message(sent_or_recieved, username, message_id=None)->Message:
    if sent_or_recieved not in [SENT, RECIEVED]:
        raise ValueError("Unexpected value for sent_or_recieved")
    user_id = get_user_id(username)
    
    if message_id:
        return get_message_by_id(user_id, message_id)
        
    if sent_or_recieved == SENT:
        message = Message.query.filter_by(sender_id=user_id).order_by(db.desc(Message.creation_date)).first()
    else:
        message = Message.query.filter_by(receiver_id=user_id).order_by(db.desc(Message.creation_date)).first()
    return message
 
def get_message_by_id(user_id, message_id)->Message:
    message = Message.query.filter(and_(
        or_(
        Message.sender_id==user_id, 
        Message.receiver_id==user_id
        ),
        Message.id==message_id
        )
        ).order_by(db.desc(Message.creation_date)).first()
    return message


def create_user(username:str, hashed_password:str)->int:
    if models.get_user(username):
        return common_utills.RegisterStatusCodes.FAILURE_USER_ALREADY_EXIST
    user = User(username=username, password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    # try: 
    #     db.session.commit()
    # except IntegrityError as e:
    #     print(e)
    #     return common_utills.RegisterStatusCodes.UNKOWN_ISSUE
    return common_utills.RegisterStatusCodes.SUCCESS
