import os
from hashlib import scrypt

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    second_name = db.Column(db.String(30))

    def __str__(self):
        result = f'{self.last_name} {self.first_name:.1}.'
        if self.second_name:
            result += f'{self.second_name:.1}.'
        return result

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'second_name': self.second_name}


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author2 = db.relationship('Author', backref='books', lazy=True)
    author2_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __str__(self):
        return self.title

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'author': str(self.author2)}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password_salt = db.Column(db.String(16), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    def hash_password(self, password: str):
        self.password_salt = os.urandom(16)
        self.password_hash = scrypt(password.encode('utf-8'), salt=self.password_salt, n=16384, r=8, p=1)

    def hash_verify(self, password: str):
        return self.password_hash == scrypt(password.encode('utf-8'), salt=self.password_salt, n=16384, r=8, p=1)
