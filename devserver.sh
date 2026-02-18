#!/bin/sh
# Activate the virtual environment in a portable way
. .venv/bin/activate

# Set Flask environment variables
export FLASK_APP=run
export FLASK_DEBUG=1

# Run the flask app. Use port from $PORT, or default to 8080.
python -m flask run --host=0.0.0.0 --port=${PORT:-8080}
