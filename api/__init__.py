from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api  # Import Api
from .celery_app import celery
from flask_cors import CORS

# Globally accessible libraries
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)  # Initialize Flask-RESTful

    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask

    with app.app_context():
        # Import parts of our application
        from . import models
        from .resources import UserListResource, UserResource, UserBioResource  # Import the resource

        # Add API resources
        api.add_resource(UserListResource, '/users')
        # Add the new resource with a dynamic ID Part
        api.add_resource(UserResource, '/users/<int:user_id>')
        # Add Bio resource
        api.add_resource(UserBioResource, '/users/<int:user_id>/generate-bio')

        return app
