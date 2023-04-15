from flask_cors import CORS
from flask import Flask, make_response, jsonify, request, session as browser_session
from flask_cors import cross_origin
from extensions import * 
from flask import Flask 
from chat_gpt_controller import chat_gpt_route_path, chat_gpt_route
from models import User, HalpreadsBooks, Bookshelf, ListedBook
import os 
import pandas as pd
import json 
import requests
from urllib.parse import urlencode
import sqlite3
from sqlalchemy.orm import noload
import openai
import math
from openai.embeddings_utils import distances_from_embeddings, indices_of_nearest_neighbors_from_distances


app = Flask(__name__)
#register modules/blueprints
app.register_blueprint(chat_gpt_route, url_prefix=f'/{chat_gpt_route_path}')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = os.environ.get('SECRET_KEY')
#app.config.from_object(config.config['development'])
CORS(app, resources={r"/*": {"origins": "http://localhost:4000"}})
# CORS(app)

API_URL = 'https://www.googleapis.com/books/v1/volumes'
API_KEY = os.getenv('API_KEY')


db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)


    

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
        if user is None:
            return {'error': 'User not found'}, 404
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

@app.route('/books')
def get_books():
    #retrieve books from the database 
    books = HalpreadsBooks.query.all()
    #update the cover_image for each book
    for book in books:
        if not book.cover_image:
            #build API request URL 
            query_params = {
                'q': f'{book.title}+inauthor:{book.author}',
                'fields': 'items(volumeInfo(imageLinks(thumbnail))),totalItems',
                'key': API_KEY
            }
            api_url = f'{API_URL}?{urlencode(query_params)}'
            #make the API request
            response = requests.get(api_url)
            response_data = json.loads(response.content)

            #check if the book was found and has a cover img 
            if 'totalItems' in response_data and response_data['totalItems'] > 0:
                cover_url = response_data['items'][0]['volumeInfo']['imageLinks']['thumbnail']

                #update in DB 
                book.cover_image = cover_url
                db.session.commit()
    #return books as JSON response
    book_dicts = [book.to_dict() for book in books]
    return make_response(jsonify(book_dicts), 200)

@app.route('/books/genre')
def get_books_by_genre():
    genre = request.args.get('genre')
    books = HalpreadsBooks.query.filter_by(genre=genre).all()
    book_list = []
    for book in books:
        book_dict = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'rating': book.rating,
            'genre': book.genre,
        }
        book_list.append(book_dict)
    return jsonify(book_list)

@app.route('/books/rating')
def get_books_by_rating():
    rating = request.args.get('rating')
    books = HalpreadsBooks.query.filter_by(rating=rating).all()
    book_list = []
    for book in books:
        book_dict = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'rating': book.rating,
            'genre': book.genre,
        }
        book_list.append(book_dict)
    return jsonify(book_list)
 
@app.route('/addbook', methods=['POST'])
def add_book():
    data = request.get_json()
    book_id = data.get('book_id')

    #get the current user 
    user = User.query.get(browser_session.get('user_id'))
    print(f"user: {user}")
    if user is None:
        return jsonify({'message': 'User not found.'}), 404
    print(f"user: {user}")
    #get or create the user's bookshelf
    bookshelf = user.bookshelves[0] if user.bookshelves else None
    if bookshelf is None:
        bookshelf = Bookshelf(user = user)
        db.session.add(bookshelf)
        db.session.commit()
    print(f"bookshelf: {bookshelf}")

    #add the book to the user's bookshelf as a ListedBook
    book = HalpreadsBooks.query.get(book_id)
    listed_book = ListedBook(book_id=book_id, bookshelf_id=bookshelf.id)
    db.session.add(listed_book)
    db.session.commit()
    print(f"listed_book: {listed_book}")
    return jsonify({'message': 'Book added to collection.'}), 201

