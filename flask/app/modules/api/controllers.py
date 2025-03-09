from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/heartbeat', methods=['GET'])
def get_heartbeat():
    return "API je aktivní"

@api.route('/users', methods=['GET'])
def get_users():
    return "Seznam uživatelů"