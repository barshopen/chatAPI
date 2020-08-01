from flask import render_template, url_for, jsonify, request, make_response
from flask_jwt_extended import jwt_required
from chat import app, models, auth
import datetime


@jwt_required
@app.route("/hello", methods=['GET'])
def hello():
    return "hello"

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)
    return auth.authenticate_user(username, password)
    

@app.route("/register", methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    password_again = request.form['password_again']
    return auth.register_user(username, password, password_again) 
    