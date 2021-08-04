from . import db
from .models import User, Message
from .models import Listings
from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app
from flask_login import login_required, current_user
from go_give.helpers import upload_file_to_s3
from go_give.config import S3_BUCKET
from .forms import MessageForm
from .models import Message
from datetime import datetime

main = Blueprint('main', __name__)
POSTS_PER_PAGE = 5


@main.route('/')
def listings():
    listings = Listings.query.all()
    return render_template('listings/index.html', listings=listings, current_user=current_user)


@main.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    listings = user.listings
    return render_template('listings/profile.html', name=current_user.firstname, user=user, listings=listings)


@main.route('/create_listing')
@login_required
def create_listing():
    return render_template('listings/create.html')


@main.route('/create_listing', methods=['POST'])
@login_required
def create_listing_post():
    name = request.form.get('name')
    description = request.form.get('description')
    location = request.form.get('location')
    email = request.form.get('email')
    file = request.files['file']
    image_url = upload_file_to_s3(file, S3_BUCKET)
    listings = Listings(name=name, description=description, location=location, email=email, author=current_user,
                        image_url=image_url)
    db.session.add(listings)
    db.session.commit()
    return redirect(url_for('main.listings'))


@main.route('/update/<int:listings_id>')
@login_required
def update_listing(listings_id):
    listings = Listings.query.get_or_404(listings_id)
    return render_template('listings/update.html', listings=listings)


@main.route('/update/<int:listings_id>', methods=['POST'])
@login_required
def update_listings(listings_id):
    listings = Listings.query.get_or_404(listings_id)
    listings.name = request.form.get('name')
    listings.description = request.form.get('description')
    listings.email = request.form.get('email')

    if request.files['file']:
        image_url = upload_file_to_s3(request.files['file'], S3_BUCKET)
        listings.image_url = image_url

    db.session.commit()

    return redirect(url_for('main.listings'))


@main.route("/searchkeyword", methods=["POST"])
def search_by_keyword():
    keyword = request.form["search-keyword"]
    listings = db.session.query(Listings).filter(Listings.description.ilike(f"%{keyword}%")).all()
    return render_template('listings/index.html', listings=listings)


# @main.route('/all')
# @login_required
# def listings():
#     listings = Listings.query.all()
#     return render_template('index.html', listings=listings)

@main.route("/listings/<int:listings_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_listing(listings_id):
    listings = Listings.query.get_or_404(listings_id)
    db.session.delete(listings)
    db.session.commit()
    return redirect(url_for('main.listings'))


@main.route('/send_message/<int:recipient>', methods=['GET', 'POST'])
@login_required
def send_message(*args, **kwargs):
    recipient = kwargs.pop('recipient', None)
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(sender_id=current_user.id, recipient_id=recipient,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash(('Your message has been sent.'))
        return redirect(url_for('main.profile', email=current_user.email))
    return render_template('send_message.html', title=('Send Message'),
                           form=form, recipient=recipient)


@main.route('/messages')
@login_required
def messages():
    messages = Message.query.filter_by(recipient_id=current_user.id).paginate(per_page=POSTS_PER_PAGE)
    from_emails = [User.query.filter_by(id=x.sender_id).first().email for x in messages.items]

    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=zip(messages.items, from_emails),
                           next_url=next_url, prev_url=prev_url)
