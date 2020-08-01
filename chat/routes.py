from flask import render_template, url_for, jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from chat import app, models, auth
import datetime


#/read/message/params?limit=None(or number)&unread_only=true&most_recent_first=true
@app.route("/read/message/", methods=['GET'], defaults={'message_id': None})
@app.route("/read/message/<int:message_id>", methods=['GET'])
@jwt_required
def get_message(message_id):
    
    return jsonify(data_provider.get_message(message_id))

@app.route("/hello", methods=['GET'])
@jwt_required
def hello():
    print(get_jwt_identity())
    return "hello"


@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    return auth.authenticate_user(username, password)
    

@app.route("/register", methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    password_again = request.form['password_again']
    return auth.register_user(username, password, password_again) 
    