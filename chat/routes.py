from flask import render_template, url_for, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from chat import app, models, auth , data_provider
import datetime
from chat import common_utills



@app.route("/read/messages/sent_only", methods=['GET'], strict_slashes=False)
@app.route("/read/messages/received_only", methods=['GET'], strict_slashes=False)
@app.route("/read/messages/unread_only", methods=['GET'], strict_slashes=False)
@app.route("/read/messages", methods=['GET'], strict_slashes=False)
@jwt_required
def get_messages():
    username = get_jwt_identity()['username']
    if str(request.url_rule) == "/read/messages/messages":
        print("read all")
        request_flag = common_utills.GetAllMessagesFlags.ALL
    elif str(request.url_rule) == "/read/messages/received_only":
        print("received only")
        request_flag = common_utills.GetAllMessagesFlags.RECEIVED_ONLY
    elif str(request.url_rule) == "/read/messages/unread_only":
        print("unread only")
        request_flag = common_utills.GetAllMessagesFlags.UNREAD_ONLY
    elif str(request.url_rule) == "/read/messages/messages/received_only":
        print("sent only")
        request_flag = common_utills.GetAllMessagesFlags.SENT_ONLY
        
    return data_provider.get_all_messages(username, request_flag)
    

@app.route("/read/message/last_sent", methods=['GET'], strict_slashes=False)
@jwt_required
def get_last_sent_message():
    username = get_jwt_identity()['username']
    return data_provider.get_last_sent_message(username)

@app.route("/read/message/last_recieved", methods=['GET'], defaults={'message_id': None}, strict_slashes=False)
@app.route("/read/message", methods=['GET'], defaults={'message_id': None}, strict_slashes=False)
@app.route("/read/message/<int:message_id>", methods=['GET'], strict_slashes=False)
@jwt_required
def get_message(message_id):
    username = get_jwt_identity()['username']
    
    return data_provider.get_message(username, message_id)

@app.route("/hello", methods=['GET'])
@jwt_required
def hello():
    return "hello"


@app.route("/login", methods=['POST'], strict_slashes=False)
def login():
    username = request.form['username']
    password = request.form['password']
    return auth.authenticate_user(username, password)
    

@app.route("/register", methods=['POST'], strict_slashes=False)
def register():
    username = request.form['username']
    password = request.form['password']
    password_again = request.form['password_again']
    return auth.register_user(username, password, password_again) 
    