from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# Init Socket.IO
socketio = SocketIO()

# Init SQLAlchemy
db = SQLAlchemy()

# Sets up our base application object
def gen_app(debug=False):
    app = Flask(__name__)
    app.debug = debug

    # Import Secrets
    from .main import k

    # SECRET_KEY generated randomly using uuidgen
    app.config['SECRET_KEY'] = k.secret_key

    # SQL Alchemy connection string and suppress warnings
    app.config['SQLALCHEMY_DATABASE_URI'] = k.sqlalchemy_database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = k.sqlalchemy_track_modifications

    # Register page blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Wrap app into socketio process
    socketio.init_app(app)

    # Wrap app into sqlalchemy process
    db.init_app(app)

    return app
