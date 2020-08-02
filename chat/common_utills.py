from enum import Enum
from chat.models import Message

class GetAllMessagesStatusCodes(Enum):
    SENT_ONLY = 0
    UNREAD_ONLY = 1
    RECEIVED_ONLY = 2
    ALL = 3

class RegisterStatusCodes(Enum):
    FAILURE_USER_ALREADY_EXIST = 0
    SUCCESS = 1
    UNKOWN_ISSUE = 2

class DeleteMessageStatusCodes:
    MESSAGE_DOES_NOT_EXIST = 1
    DELETE_FAILED = 2
    DELETE_SUCCESSFUL = 3

def message_to_dict(message:Message)->dict:
    return {
    'message_id': message.id,
    'creation_date': message.creation_date.strftime(r'%m/%d/%y %H:%M:%S'),
    'subject': message.subject,
    'message': message.message,
    'sender': message.sender.username,
    'receiver': message.receiver.username
    }