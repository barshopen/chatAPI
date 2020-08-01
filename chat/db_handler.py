from chat import db
from chat.models import User
from sqlalchemy.exc import IntegrityError


SUCCESS = 1
FAILURE_USER_EXIST = 2


def create_user(username:str, hashed_password:str)->int:
    user = User(username=username, password_hash=hashed_password)
    db.session.add(user)
    try: 
        db.session.commit()
    except IntegrityError as e:
        print(e)
        return FAILURE_USER_EXIST
    return SUCCESS

def find_user(username:str)-> User:
    return User.query.filter_by(username=username).first()
