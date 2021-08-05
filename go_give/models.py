from . import db
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    location = db.Column(db.String(100))
    image_url = db.Column(db.String(100), nullable=False)

    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    listings = db.relationship('Listings', backref='author', lazy=True)
    liked = db.relationship('PostLike', foreign_keys='PostLike.user_id', backref='author', lazy='dynamic')

    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def like_post(self, listings):
        if not self.has_liked_post(listings):
            like = PostLike(user_id=self.id, listings_id=listings.id)
            db.session.add(like)

    def unlike_post(self, listings):
        if self.has_liked_post(listings):
            PostLike.query.filter_by(
                user_id=self.id,
                listings_id=listings.id).delete()

    def has_liked_post(self, listings):
        return PostLike.query.filter(
            PostLike.user_id == self.id,
            PostLike.listings_id == listings.id).count() > 0

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()


class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    listings_id = db.Column(db.Integer, db.ForeignKey('listings.id'))


class Listings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_url = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    likes = db.relationship('PostLike', backref='listings', lazy='dynamic')
    image_url = db.Column(db.String(100), nullable=False)
    categories = db.Column(db.String(20))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    email = db.Column(db.String(100))

    def __repr__(self):
        return '<Message {}>'.format(self.body)
