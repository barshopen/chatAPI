from enum import Enum
from chat.models import Message

class GetAllMessagesFlags(Enum):
    SENT_ONLY = 0
    UNREAD_ONLY = 1
    RECEIVED_ONLY = 2
    ALL = 3
    
def message_to_dict(message:Message)->dict:
    return {
    'message_id': message.id,
    'creation_date': message.creation_date.strftime(r'%m/%d/%y %H:%M:%S'),
    'subject': message.subject,
    'message': message.message,
    'sender': message.sender.username,
    'receiver': message.receiver.username
    }