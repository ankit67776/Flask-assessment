from flask import request
from flask_restful import Resource
from .models import User
from .schemas import UserSchema
from . import db
from .tasks import generate_bio

class UserListResource(Resource):
    """Resource for handling lists of Users."""

    def get(self):
        """Gets all users."""
        users = User.query.all()
        schema = UserSchema(many=True)
        return schema.dump(users)

    def post(self):
        """Creates a new user."""
        schema = UserSchema()
        try:
            data = schema.load(request.get_json())
        except Exception as e:
            return {'message': str(e)}, 400

        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()

        return schema.dump(user), 201

class UserResource(Resource):
    """Resource for handling a single User."""

    def get(self, user_id):
        """Gets a single user by ID."""
        user = db.get_or_404(User, user_id)
        schema = UserSchema()
        return schema.dump(user)

    def put(self, user_id):
        """Updates a user."""
        user = db.get_or_404(User, user_id)
        schema = UserSchema()
        try:
            # We use `partial=True` to allow partial updates
            data = schema.load(request.get_json(), partial=True)
        except Exception as e:
            return {'message': str(e)}, 400

        # Update fields if they are present in the request
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()

        return schema.dump(user)

    def delete(self, user_id):
        """Deletes a user."""
        user = db.get_or_404(User, user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class UserBioResource(Resource):
    def post(self, user_id):
        """
        Triggers the AI bio generation task for a user.
        """

        keywords = ["professional", "Python", "flask"]

        task = generate_bio.delay(user_id, keywords)

        return {'message': 'Bio generation started.', 'task_id': task.id}, 202