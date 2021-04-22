import os
from hashlib import scrypt

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    second_name = db.Column(db.String(30))
    stud_id = db.Column(db.Integer, nullable=False)
    group = db.relationship('Group', backref='students', lazy=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __str__(self):
        result = f'{self.last_name} {self.first_name:.1}.'
        if self.second_name:
            result += f'{self.second_name:.1}.'
        return result

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'second_name': self.second_name, 'group': str(self.group)}

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'year': self.year, 'status':self.status }
