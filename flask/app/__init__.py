import os
from flask import Flask
from app.modules.auth.controllers import auth
from app.modules.dashboard.controllers import dashboard
from app.modules.api.controllers import api
from app.controllers.main import main

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__, 
                template_folder=os.path.join(BASE_DIR, "views/templates"),
                static_folder=os.path.join(BASE_DIR, "static"))

    app.config.from_object("config")

    db.init_app(app)
    login_manager.init_app(app)

    from app.modules.auth.models import User  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Funkce, která získá uživatele podle ID
    
    with app.app_context():
        db.create_all()  # Vytvoří tabulky, pokud neexistují
    
    # Registrace blueprintů
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    return app
