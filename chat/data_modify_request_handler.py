from chat import db_handler, common_utills
from flask import jsonify

def write_message(sender_username:str, receiver_username:str, subject:str, message:str):
    if not(receiver_username and subject and message):
        return "Please make sure to include the receiver, subject and message fields in your request", 409
    
    message = db_handler.write_message(sender_username, receiver_username, subject, message)
    
    if not message:
        return "The server encountered an unexpected condition which prevented it from fulfilling the request, please try agian later", 500
    
    return jsonify(common_utills.message_to_dict(message)), 200

def write_message(username:str, message_id:int):
    pass