from flask import jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from typing import Tuple
from flask_jwt_extended import create_access_token
import datetime
from chat import db_handler, bcrypt, common_utills
from chat.models import User

EXPIRED_IN = datetime.timedelta(hours=2) 

def register_user(username:str, password:str, password_again:str)-> int:
    """@ret http status code 200, 409, 422
    200 : user created.
    409 : username already exist.
    422 : something's wrong with your password/ username
    """
    # this shouldn't be here...
    if not (username and password and password_again):
        return "Please make sure to include the following params: username, password, password_again", 422
    elif len(password)<8:
        return "Password should be more then 8 characters long and password_again should match password", 422
    elif password != password_again:
        return "Password should match password_again field", 422
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    status_code = db_handler.create_user(username, hashed_password) 
    if status_code == common_utills.RegisterStatusCodes.FAILURE_USER_ALREADY_EXIST:
        return "Username already exist", 409
    elif status_code == common_utills.RegisterStatusCodes.UNKOWN_ISSUE:
        return "The server encountered an unexpected condition which prevented it from fulfilling the request, please try agian later", 500
    
    return jsonify({"username": username}), 201

def authenticate_user(username:str, passowrd:str)->Tuple:
    user = User.query.filter_by(username=username).first()
    if not(user and user.check_password(passowrd)):
        return "Wrong credentials", 409 
    
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity={"username":user.username}, expires_delta=EXPIRED_IN)
    return jsonify({"token": access_token}), 200
    