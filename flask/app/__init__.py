import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy     # type: ignore
from flask_login import LoginManager        # type: ignore

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__, 
                template_folder=os.path.join(BASE_DIR, "views/templates"),
                static_folder=os.path.join(BASE_DIR, "static"))

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.controllers.auth_controller import auth
    from app.controllers.main import main
    from app.models.user_model import Pacient, Lekar

    @login_manager.user_loader
    def load_user(user_id):
        with current_app.app_context():  # 📌 Použití `current_app` namísto `app`
            session = db.session
            user = session.get(Pacient, int(user_id))
            if not user:
                user = session.get(Lekar, int(user_id))
            return user
    
    with app.app_context():
        db.create_all()  # Vytvoří tabulky, pokud neexistují

    # Registrace blueprintů
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    
    from app.controllers.api_controller import api 
    app.register_blueprint(api, url_prefix="/api")  
    return app
