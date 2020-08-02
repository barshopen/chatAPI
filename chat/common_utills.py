from enum import Enum

class GetAllMessagesFlags(Enum):
    SENT_ONLY = 0
    UNREAD_ONLY = 1
    RECEIVED_ONLY = 2
    ALL = 3
