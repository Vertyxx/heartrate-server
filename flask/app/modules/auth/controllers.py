from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

#prozatim
@auth.route('/')
def home():
    return render_template("homepage.html")