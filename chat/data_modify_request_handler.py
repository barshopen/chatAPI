from chat import db_handler, common_utills
from flask import jsonify

def write_message(sender_username:str, receiver_username:str, subject:str, message:str):
    if not(receiver_username and subject and message):
        return "Please make sure to include the receiver, subject and message fields in your request", 409
    
    message = db_handler.write_message(sender_username, receiver_username, subject, message)
    
    if not message:
        return "The server encountered an unexpected condition which prevented it from fulfilling the request, please try agian later", 500
    
    return jsonify(common_utills.message_to_dict(message)), 200

def delete_message(username:str, message_id:int):
    if not message_id:
        return "Please specify message_id", 409
    
    status = db_handler.delete_message(username, message_id)
    if status == common_utills.DeleteMessageStatusCodes.DELETE_FAILED:
        return "The server encountered an unexpected condition which prevented it from fulfilling the request, please try agian later", 500
    elif status == common_utills.DeleteMessageStatusCodes.MESSAGE_DOES_NOT_EXIST:
        return "Message doesn't exist", 404
    elif status == common_utills.DeleteMessageStatusCodes.DELETE_SUCCESSFUL:
        return "Message deleted successfully", 200
