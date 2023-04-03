from flask import Flask, make_response, jsonify, request, session as browser_session
from flask_cors import CORS
from flask_cors import cross_origin
from models import db, User
from extensions import * 

import openai
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = os.environ.get('SECRET_KEY')
CORS(app, resources={r"/*": {"origins": "http://localhost:4000"}})
# CORS(app)


db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter(User.username == username).first()

    if not user:
        return jsonify({'error': 'invalid login'}), 404

    if not user.authenticate(password):
        return jsonify({'error': 'invalid login'}), 404

    browser_session['user_id'] = user.id
    return jsonify(user.to_dict()), 201

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    new_user = User(
        username=data.get('username'),
    )
    new_user.password_hash = data.get('password')
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/check_session', methods=['GET'])
def check_session():
    if browser_session.get('user_id'):
        user = User.query.filter(User.id == browser_session['user_id']).first()
        return user.to_dict(), 200
    return {'error': '401 Unauthorized'}, 404
        

@app.route('/logout', methods=['DELETE'])
def logout():
    browser_session.pop('user_id')
    return jsonify({}), 204

@app.route('/authorized')
def authorized():
    user_id = browser_session.get('user_id')
    user = User.query.filter(User.id == user_id).first()

    if not user:
        return jsonify({'error': 'not authorized'}), 401
    
    return jsonify(user.to_dict()), 200

@app.route('/')
def root():
    return ''

if __name__ == '__main__':
    app.run(port=5555, debug = True)
