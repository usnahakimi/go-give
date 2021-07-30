from . import db
from .models import User
from .models import Listings
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from go_give.helpers import upload_file_to_s3
from go_give.config import S3_BUCKET
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    listings = user.listings
    return render_template('profile.html', name=current_user.firstname, user=user, listings=listings)

@main.route('/create_listing')
@login_required
def create_listing():
    return render_template('listings/create.html')

@main.route('/create_listing', methods=['POST'])
@login_required
def create_listing_post(): 
    name = request.form.get('name')
    description = request.form.get('description')
    email = request.form.get('email')
    file = request.files['file']
    image_url = upload_file_to_s3(file, S3_BUCKET )
    listings = Listings(name=name, description=description, email=email, author=current_user, image_url=image_url )
    db.session.add(listings)
    db.session.commit()
    return redirect(url_for('main.listings'))

@main.route('/all')
@login_required
def listings():
    listings = Listings.query.all()
    return render_template('listings/index.html', listings=listings)

# @main.route("/listings/<int:listings_id>/delete", methods=['GET', 'POST'])
# @login_required
# def delete_listing(listings_id):
#     listing = Listings.query.get_or_404(listings_id)
#     db.session.delete(listing)
#     db.session.commit()
#     return redirect(url_for('main.listings'))