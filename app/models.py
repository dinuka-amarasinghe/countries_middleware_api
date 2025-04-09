from datetime import datetime
from flask_login import UserMixin

from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'


import bcrypt
from app import db
from datetime import datetime

class APIKey(db.Model):
    __tablename__ = 'api_keys'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), unique=True, nullable=False)  # This will store the hashed API key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='api_keys')

    def __repr__(self):
        return f'<APIKey {self.key}>'

    @staticmethod
    def hash_key(api_key):
        """ Hash the API key before saving it """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(api_key.encode('utf-8'), salt)
