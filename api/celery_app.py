from celery import Celery

# Create the celery instance.

celery = Celery(__name__,
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0',
                include=['api.tasks']) 
