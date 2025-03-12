import os
from flask import Flask
from app.controllers.auth_controller import auth
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

    from app.models import user_model  

    @login_manager.user_loader
    def load_user(user_id):
        return user_model.query.get(int(user_id))  # Funkce, která získá uživatele podle ID
    
    with app.app_context():
        db.create_all()  # Vytvoří tabulky, pokud neexistují
    
    # Registrace blueprintů
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    return app
