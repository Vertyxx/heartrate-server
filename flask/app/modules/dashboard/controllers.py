from flask import Blueprint

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def home():
    return "Hlavní stránka"