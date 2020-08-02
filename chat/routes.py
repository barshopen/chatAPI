from chat import app, models, auth, data_provide_request_handler, data_modify_request_handler, common_utills
from flask import render_template, url_for, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

@app.route("/delete/message/<int:message_id>", methods=['DELETE'], strict_slashes=False)
@jwt_required
def delete_message(message_id:int):
    username = get_jwt_identity()['username']

    return data_modify_request_handler.delete_message(username, message_id)


@app.route("/write/message", methods=['POST'], strict_slashes=False)
@jwt_required
def write_message():
    username = get_jwt_identity()['username']
    
    form = request.form.to_dict()
    receiver = form.get("receiver")
    subject = form.get("subject")
    message = form.get("message")
    
    return data_modify_request_handler.write_message(username, receiver, subject, message)

@app.route("/read/messages/sent_only", methods=['GET'], strict_slashes=False)
@app.route("/read/messages/received_only", methods=['GET'], strict_slashes=False)
@app.route("/read/messages/unread_only", methods=['GET'], strict_slashes=False)
@app.route("/read/messages", methods=['GET'], strict_slashes=False)
@jwt_required
def get_messages():
    username = get_jwt_identity()['username']
    if str(request.url_rule) == "/read/messages":
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
        
    return data_provide_request_handler.get_all_messages(username, request_flag)
    

@app.route("/read/message/last_sent", methods=['GET'], strict_slashes=False)
@jwt_required
def get_last_sent_message():
    username = get_jwt_identity()['username']
    return data_provide_request_handler.get_last_sent_message(username)

@app.route("/read/message/last_recieved", methods=['GET'], defaults={'message_id': None}, strict_slashes=False)
@app.route("/read/message", methods=['GET'], defaults={'message_id': None}, strict_slashes=False)
@app.route("/read/message/<int:message_id>", methods=['GET'], strict_slashes=False)
@jwt_required
def get_message(message_id):
    username = get_jwt_identity()['username']
    
    return data_provide_request_handler.get_message(username, message_id)

@app.route("/hello", methods=['GET'])
@jwt_required
def hello():
    return "hello"


@app.route("/login", methods=['POST'], strict_slashes=False)
def login():
    form = request.form.to_dict()
    username = form.get('username')
    password = form.get('password')
    return auth.authenticate_user(username, password)
    

@app.route("/register", methods=['POST'], strict_slashes=False)
def register():
    form = request.form.to_dict()
    username = form.get('username')
    password = form.get('password')
    password_again = form.get('password_again')
    return auth.register_user(username, password, password_again) 
    