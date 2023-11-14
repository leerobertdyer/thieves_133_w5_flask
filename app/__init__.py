from flask import Flask
from config import Config
from flask_login import LoginManager
from app.models import db
from flask_migrate import Migrate
from .models import User

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)
migrate = Migrate(app, db)

from .blueprints.auth import auth
app.register_blueprint(auth)
from .blueprints.main import main
app.register_blueprint(main)
from .blueprints.errors import errors
app.register_blueprint(errors)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

