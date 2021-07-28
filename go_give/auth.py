from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        location = request.form.get('location')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            return redirect(url_for('auth.register'))

        new_user = User(email=email, firstname=firstname, lastname=lastname, 
        location=location, username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth.route('/login', methods=("GET", "POST"))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(email, password)

        return redirect(url_for('main.profile'))
    
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    return "Log out"