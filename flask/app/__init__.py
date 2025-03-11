from flask import Flask
from app.modules.auth.controllers import auth
from app.modules.dashboard.controllers import dashboard
from app.modules.api.controllers import api

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    app.config.from_object("config")

    db.init_app(app)
    login_manager.init_app(app)

    from app.controllers.main import main
    app.register_blueprint(main)

    # registration of blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    return app