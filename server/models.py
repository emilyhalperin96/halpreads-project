from extensions import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from dataclasses import dataclass 


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)

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
