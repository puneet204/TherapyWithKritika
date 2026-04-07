from flask import Blueprint, render_template

validate = Blueprint('validate', __name__)

@validate.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@validate.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template("logout.html")