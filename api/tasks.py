from .celery_app import celery  

@celery.task
def generate_bio(user_id, keywords):
    """
    A placeholder for our AI bio generation task.
    """
    # AI logic 
    print(f"Generating bio for user {user_id} with keywords: {keywords}")
    return "This is a placeholder bio."
