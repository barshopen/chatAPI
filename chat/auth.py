from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from typing import Tuple
from flask_jwt_extended import create_access_token
import datetime
from chat import db_handler, bcrypt
from chat.models import User

EXPIRED_IN = datetime.timedelta(minutes=30) 

def register_user(username:str, password:str, password_again:str)-> int:
    """@ret http status code 200, 409, 422
    200 : user created.
    409 : username already exist.
    422 : something's wrong with your password/ username
    """
    # this shouldn't be here...
    if len(password)<8 or password != password_again:
        return "Password should be more then 8 characters long", 422
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    if db_handler.create_user(username, hashed_password) == db_handler.FAILURE_USER_EXIST:
        return "Username already exist", 409
    
    return username, 200

def authenticate_user(username:str, passowrd:str)->Tuple:
    user = User.query.filter_by(username=username).first()
    if not(user and user.check_password(passowrd)):
        return "Wrong credentials", 409 
    expires = datetime.timedelta(days=7)
    print(user.username)
    access_token = create_access_token(identity={"username":user.username}, expires_delta=EXPIRED_IN)
    return jsonify({"token": access_token}), 200
    