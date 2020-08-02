from chat.models import db, User, Message
from typing import List, Tuple
from flask import jsonify
from chat import db_handler



def get_all_messages()->List[dict]:
    return [to_json(message) for message in Message.query.all()]

def get_last_sent_message(username:str)->Tuple[str, int]:
    answer = db_handler.get_message(db_handler.SENT, username)
    if not answer:
        return "No messages found", 204

    return to_json(answer), 200


def get_message(username:str, message_id:int)->dict:
    answer = db_handler.get_message(db_handler.RECIEVED, username, message_id)
                                    
    if not answer:
        return "No messages found", 204

    return to_json(answer), 200


def to_json(message:Message)->dict:
    return jsonify({
    'message_id': message.id,
    'creation_date': message.creation_date.strftime(r'%m/%d/%y %H:%M:%S'),
    'subject': message.subject,
    'message': message.message,
    'sender': message.sender.username,
    'receiver': message.receiver.username
    })