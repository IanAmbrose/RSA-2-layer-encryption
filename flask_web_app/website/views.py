from flask import Blueprint, render_template

views = Blueprint('views', __name__)
# decorator, when ever you hit this route it calls the function  below. THis is defined by '/' 


@views.route('/') 
def home():
    return render_template("home.html")


