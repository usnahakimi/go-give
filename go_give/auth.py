from flask import Blueprint, render_template, url_for, request, redirect
from flask.helpers import flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from go_give.helpers import upload_file_to_s3
from go_give.config import S3_BUCKET


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
        file = request.files['file']
        image_url = upload_file_to_s3(file, S3_BUCKET)
        error = None

        if not email:
            error = "Email is required."
        elif not username:
            error = "Username is required."
        elif not firstname:
            error = "First name is required"
        elif not lastname:
            error = "Last name is required"
        elif not location:
            error = "Location is required"
        elif not password:
            error = "Password is required."
        # elif User.find(username) is not None:
        #     error = f"User {username} is already registered."
        elif password.isalpha():
            error = "Password must contain numbers and/or symbols"
        elif len(password) < 8:
            error = "Password must be more than 8 characters long"

        user = User.query.filter_by(email=email).first()

        if user:
            return redirect(url_for('main.profile'))

        if error is None:
            new_user = User(email=email, firstname=firstname, lastname=lastname, 
            location=location, username=username, password=generate_password_hash(password, method='sha256'), image_url = image_url)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('main.profile'))
        
        flash(error)

    return render_template('auth/register.html')

@auth.route('/login', methods=("GET", "POST"))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        error = None
        user = User.query.filter_by(email=email).first()

        if not user:
            error = "Email does not exist!"
        elif not user or not check_password_hash(user.password, password):
            error = "Incorrect password."
            # return render_template('auth/login.html')

        if error is None:
            login_user(user, remember=remember)
            return redirect(url_for('main.profile'))
        
        flash(error)

        
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.listings'))