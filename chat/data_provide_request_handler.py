from typing import List, Tuple
from flask import jsonify
from chat import db_handler, common_utills
from chat.models import Message

def get_all_messages(username:str, request_flag:int)->List[dict]:
    answer = db_handler.get_all_messages(username, request_flag)
    for message in answer:
        message.mark_as_read_if_called_from_receiver(username)
    if not answer:
        return "No messages found", 204
    return jsonify([common_utills.message_to_dict(message) for message in answer]), 200

def get_last_sent_message(username:str)->Tuple[str, int]:
    answer = db_handler.get_message(db_handler.SENT, username)
    
    if not answer:
        return "No messages found", 204

    return jsonify(common_utills.message_to_dict(answer)), 200


def get_message(username:str, message_id:int)->dict:
    answer = db_handler.get_message(db_handler.RECIEVED, username, message_id)
        
    if not answer:
        return "No messages found", 204
    
    answer.mark_as_read_if_called_from_receiver(username)                        
    return jsonify(common_utills.message_to_dict(answer)), 200


