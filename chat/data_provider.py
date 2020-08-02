from chat.models import db, User, Message
from typing import List, Tuple
from flask import jsonify
from chat import db_handler

def get_all_messages(username:str, request_flag:int)->List[dict]:
    answer = db_handler.get_all_messages(username, request_flag)
    if not answer:
        return "No messages found", 204
    return jsonify([to_dict(message) for message in answer]), 200

def get_last_sent_message(username:str)->Tuple[str, int]:
    answer = db_handler.get_message(db_handler.SENT, username)
    if not answer:
        return "No messages found", 204

    return jsonify(to_dict(answer)), 200


def get_message(username:str, message_id:int)->dict:
    answer = db_handler.get_message(db_handler.RECIEVED, username, message_id)
                                    
    if not answer:
        return "No messages found", 204

    return jsonify(to_dict(answer)), 200


def to_dict(message:Message)->dict:
    return {
    'message_id': message.id,
    'creation_date': message.creation_date.strftime(r'%m/%d/%y %H:%M:%S'),
    'subject': message.subject,
    'message': message.message,
    'sender': message.sender.username,
    'receiver': message.receiver.username
    }