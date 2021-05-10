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

    def to_dict_without_groups(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'second_name': self.second_name, 'stud_id': self.stud_id}

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'second_name': self.second_name, 'stud_id': self.stud_id, 'group': self.group.to_dict_without_students()}

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False)

    def to_dict_without_students(self):
        return {'id': self.id, 'name': self.name, 'year': self.year, 'status': self.status}

    def to_dict(self):
        students = []
        for s in self.students:
            students.append(s.to_dict_without_groups())
        return {'id': self.id, 'name': self.name, 'year': self.year, 'status':self.status, 'students':students}
