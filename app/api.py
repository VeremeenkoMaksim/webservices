from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.models import db, Book, User, Author


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


class BooksResource(Resource):
    @jwt_required()
    def get(self):
        result = Book.query.all()
        return [b.to_dict() for b in result]

    def post(self):
        data = request.get_json()
        db.session.add(Book(title=data['title'], author=data['author']))
        db.session.commit()
        return {'success': True}


class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return book.to_dict()

    def put(self, book_id):
        data = request.get_json()
        book = Book.query.get(book_id)
        book.title = data.get('title')
        book.author = data.get('author')
        db.session.add(book)
        db.session.commit()
        return {'success': True}

    def delete(self, book_id):
        book = Book.query.get(book_id)
        db.session.delete(book)
        db.session.commit()
        return {'success': True}


class AuthorsResource(Resource):
    @jwt_required()
    def get(self):
        result = Author.query.all()
        return [b.to_dict() for b in result]

    def post(self):
        data = request.get_json()
        db.session.add(Author(last_name=data['last_name'], first_name=data['first_name'], second_name=data['second_name']))
        db.session.commit()
        return {'success': True}


class AuthorResource(Resource):
    def get(self, author_id):
        author = Author.query.get_or_404(author_id)
        return author.to_dict()

    def put(self, author_id):
        data = request.get_json()
        author = Author.query.get(author_id)
        author.last_name = data.get('last_name')
        author.first_name = data.get('first_name')
        author.second_name = data.get('second_name')
        db.session.add(author)
        db.session.commit()
        return {'success': True}

    def delete(self, author_id):
        author = Author.query.get(author_id)
        db.session.delete(author)
        db.session.commit()
        return {'success': True}
