from extensions import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from dataclasses import dataclass 

class Bookshelf(db.Model):
    __tablename__ = 'bookshelf'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class ListedBook(db.Model):
    __tablename__ = 'listed_book'
    id = db.Column(db.Integer, primary_key=True)
    read = db.Column(db.Boolean, default=False)
    bookshelf_id = db.Column(db.Integer, db.ForeignKey('bookshelf.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('halpreads.id'))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)
    bookshelves = db.relationship('Bookshelf', backref='user', lazy=True)

    @hybrid_property
    def password_hash(self):
        return self._password_hash


    @password_hash.setter 
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
        }

class HalpreadsBooks(db.Model):
    __tablename__ = "halpreads"
   # __bind_key__ = 'halpreads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    genre = db.Column(db.String)
    rating = db.Column(db.Float)
    summary = db.Column(db.String)
    cover_image = db.Column(db.String(200), nullable=True)
    listed_books = db.relationship('ListedBook', backref='book')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'rating': self.rating,
            'summary': self.summary,
            'cover_image': self.cover_image
        }


@dataclass
class MessageRequestDTO:
    question: str 

    @staticmethod # can remove self 
    def new_instance_from_flask_body(data:dict) ->'MessageRequestDTO':
        if 'question' not in data:
            raise Exception('question attribute not found')
        
        return MessageRequestDTO(
            question=data['question']
        )
