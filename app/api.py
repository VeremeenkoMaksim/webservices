from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.models import db, Student, Group


# class UsersResource(Resource):
#     def post(self):
#         data = request.get_json()
#         user = User.query.filter_by(username=data['username']).first()
#         if user and user.hash_verify(data['password']):
#             token = ''  # TODO: create token
#             return {
#                 'success': True,
#                 'token': token
#             }
#         return {'success': False}

class GroupsResource(Resource):
    def get(self):
        result = Group.query.all()
        return [g.to_dict() for g in result]

    def post(self):
        data = request.get_json()
        db.session.add(Group(name=data['name'], year=data['year'], status=data['status']))
        db.session.commit()
        return {'success': True}

class GroupResource(Resource):
    def get(self, group_id):
        group = Group.query.get_or_404(group_id)
        return group.to_dict()

    def put(self, group_id):
        data = request.get_json()
        group = Group.query.get(group_id)
        group.name = data.get('name')
        group.year = data.get('year')
        group.status = data.get('status')
        db.session.add(group)
        db.session.commit()
        return {'success': True}

    def delete(self, group_id):
        group = Group.query.get(group_id)
        db.session.delete(group)
        db.session.commit()
        return {'success': True}

class StudentsResource(Resource):
    def get(self):
        result = Student.query.all()
        return [s.to_dict() for s in result]

    def post(self):
        data = request.get_json()
        groups = Group.query.all()
        group = Group(name='', year=0, status='')
        for g in groups:
            if data['group'] == g.name:
                group = g
        if group.name == '':
            return {'success': False}
        s = Student(last_name=data['last_name'], first_name=data['first_name'], second_name=data['second_name'], stud_id=data['stud_id'])
        s.group = group
        db.session.add(s)
        db.session.commit()
        return {'success': True}

class StudentResource(Resource):
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        return student.to_dict()

    def put(self, student_id):
        data = request.get_json()
        groups = Group.query.all()
        group = Group(name='', year=0, status='')
        for g in groups:
            if data.get('group') == g.name:
                group = g
        if group.name == '':
            return {'success': False}
        student = Student.query.get(student_id)
        student.last_name = data.get('last_name')
        student.first_name = data.get('first_name')
        student.second_name = data.get('second_name')
        student.stud_id = data.get('stud_id')
        student.group = group
        db.session.add(student)
        db.session.commit()
        return {'success': True}

    def delete(self, student_id):
        student = Student.query.get(student_id)
        db.session.delete(student)
        db.session.commit()
        return {'success': True}
