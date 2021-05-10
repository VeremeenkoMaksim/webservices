from flask import Flask, send_from_directory, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import JWTManager, create_access_token
from flask_migrate import Migrate
from flask_restful import Api

from app.api import GroupsResource, GroupResource, StudentResource, StudentsResource
from app.models import db, Student, Group


def send_client(filename='index.html'):
    return send_from_directory('static', filename)

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'abc'
    app.config['JWT_SECRET_KEY'] = 'abc'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_envvar('APP_CONFIG', True)

    db.init_app(app)
    Migrate(app, db, render_as_batch=('sqlite' in app.config['SQLALCHEMY_DATABASE_URI']))

    admin = Admin(app)
    admin.add_view(ModelView(Student, db.session))
    admin.add_view(ModelView(Group, db.session))

    JWTManager(app)

    app.add_url_rule('/', view_func=send_client)
    app.add_url_rule('/<path:filename>', view_func=send_client)

    api = Api(app)
    api.add_resource(GroupsResource, '/group/')
    api.add_resource(GroupResource, '/group/<int:group_id>/')
    api.add_resource(StudentsResource, '/student/')
    api.add_resource(StudentResource, '/student/<int:student_id>/')

    return app
