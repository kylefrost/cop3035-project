from flask import Blueprint

# Declare main page blueprint
main = Blueprint('main', __name__)

# Load page routes and socket events
from . import routes, events, secrets

# Create secrets object
k = secrets.Secrets()
