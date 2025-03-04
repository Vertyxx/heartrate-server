from flask import Flask
from app.modules.auth.controllers import auth
from app.modules.dashboard.controllers import dashboard
from app.modules.api.controllers import api

def create_app():
    app = Flask(__name__)

    # registration of blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')

    return app