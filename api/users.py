import flask_restful
from flask import jsonify, make_response, request
from flask_restful import reqparse

from data import db_session
from data.users import User


class UserResource(flask_restful.Resource):
    def get(self, user_id):
        user = db_session.create_session().get(User, user_id)
        if user is None:
            return flask_restful.abort(404,
                                       message=f"User with id {user_id} not found",
                                       error=404)
        return user.to_dict()

    def delete(self, user_id):
        sess = db_session.create_session()
        user = sess.get(User, user_id)
        if user is None:
            return flask_restful.abort(404,
                                       message=f"User with id {user_id} not found",
                                       error=404)
        sess.delete(user)
        sess.commit()
        return {"message": "User deleted"}, 204


class UserListResource(flask_restful.Resource):
    def __init__(self):
        super().__init__()
        add_user_parse = reqparse.RequestParser()
        add_user_parse.add_argument('surname')
        add_user_parse.add_argument('name')
        add_user_parse.add_argument('age')
        add_user_parse.add_argument('position')
        add_user_parse.add_argument('speciality')
        add_user_parse.add_argument('address')
        add_user_parse.add_argument('email')
        add_user_parse.add_argument('password')
        self.add_user_args = add_user_parse

    def get(self):
        users = db_session.create_session().query(User).all()
        return {"users": [u.to_dict() for u in users]}

    def post(self):
        args = self.add_user_args.parse_args()
        sess = db_session.create_session()
        if sess.query(User).filter(User.email == args['email']).first():
            return flask_restful.abort(400,
                                       message=f"User with email {args['email']} already exists!")
        u = User()
        u.name = args['name']
        u.surname = args['surname']
        u.age = args['age']
        u.position = args['position']
        u.speciality = args['speciality']
        u.address = args['address']
        u.email = args['email']
        u.set_password(args['password'])
        sess.add(u)
        sess.commit()
        return u.to_dict(), 201
