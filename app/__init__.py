from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Import blueprints and models here to avoid circular imports
    from app.models import User  # Import after db initialization
    from .auth.routes import auth_bp
    from .notes.routes import notes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Import User here to avoid circular import
    return User.query.get(int(user_id))
