from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

#prozatim
@auth.route('/')
def home():
    return render_template("../views/templates/homepage.html")