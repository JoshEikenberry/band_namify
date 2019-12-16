from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class BandName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    band_name = db.Column(db.String(256), unique=True)
    submit_date = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.Column(db.Integer, default=0)
    reports = db.Column(db.Integer, default=0)
    blacklisted = db.Column(db.Boolean, default=False)
    whitelisted = db.Column(db.Boolean, default=True)

    def all_bands_submitted(self):
        all_bands = BandName.query.order_by(BandName.submit_date).all()
        return all_bands

    def random_bands(self):
        random_bands = BandName.query.order_by(BandName.submit_date).all()
        return random_bands

    def upvote(self, band_id):
        band = BandName.query.filter_by(id=band_id).first()
        band.votes = band.votes + 1
        db.session.commit()
        return band_id

    def report_band(self, band_id):
        band = BandName.query.filter_by(id=band_id).first()
        band.reports = band.reports + 1
        db.session.commit()
        return band_id

    def blacklist(self, band_id):
        band = BandName.query.filter_by(id=band_id).first()
        if band.blacklisted is False:
            band.blacklisted = True
        else:
            band.blacklisted = False
        db.session.commit()
        return band_id

    def whitelist(self, band_id):
        band = BandName.query.filter_by(id=band_id).first()
        if band.whitelisted is True:
            band.whitelisted = False
        else:
            band.whitelisted = True
        db.session.commit()
        return band_id

    def __repr__(self):
        return '<id: {}, Band Name: {}, reports: {}>'.format(self.id, self.band_name, self.reports)
