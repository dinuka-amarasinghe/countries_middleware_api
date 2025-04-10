from datetime import datetime
from flask_login import UserMixin
import bcrypt
from app import db
from datetime import datetime

from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<User {self.email}>'


class APIKey(db.Model):
    __tablename__ = 'api_keys'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), unique=True, nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship('User', backref='api_keys')

    def __repr__(self):
        return f'<APIKey {self.key}>'

    @staticmethod
    def hash_key(api_key):
        """ Hash the API key before saving it """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(api_key.encode('utf-8'), salt)


class APIUsage(db.Model):
    __tablename__ = 'api_usage'

    id = db.Column(db.Integer, primary_key=True)
    api_key_id = db.Column(db.Integer, db.ForeignKey('api_keys.id'), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    endpoint = db.Column(db.String(256), nullable=False) 
    timestamp = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref='api_usages')
    api_key = db.relationship('APIKey', backref='usage', lazy=True)

    def __repr__(self):
        return f'<APIUsage api_key_id={self.api_key_id}, user_id={self.user_id}, endpoint={self.endpoint}, timestamp={self.timestamp}>'


