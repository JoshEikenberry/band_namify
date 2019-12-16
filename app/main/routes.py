from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from app import db, limiter
from app.main.forms import BandNameForm
from app.models import BandName
from app.main import bp
from sqlalchemy.sql.expression import func


@bp.route('/explore')
def explore():
    bands = BandName.query.filter(BandName.blacklisted != True).order_by(BandName.votes.desc()).limit(25)
    return render_template('index.html', title='Top 25 Bands by number of Votes', bands=bands)


@bp.route('/upvote/<b32:band_id>')
@limiter.limit('1/second')
def upvote(band_id):
    upvoted_band = BandName.query.filter_by(id=band_id).first()
    flash(str(upvoted_band.band_name) + ' thanks you for your support.')
    upvoted_band.upvote(band_id=band_id)
    return redirect(url_for('main.random_band',))


@bp.route('/report/<b32:band_id>')
@limiter.limit('5/minute')
def report(band_id):
    reported_band = BandName.query.filter_by(id=band_id).first()
    flash(str(reported_band.band_name) + ' has been reported as being offensive.')
    reported_band.report_band(band_id=band_id)
    return redirect(url_for('main.random_band',))


@bp.route('/admin/blacklist')
@login_required
def admin_blacklist():
    reported_bands = BandName.query.filter(BandName.reports >= 1).order_by(BandName.reports.desc()).all()
    return render_template('admin/blacklist.html', bands=reported_bands)


@bp.route('/blacklist/<b32:band_id>')
@login_required
def blacklist(band_id):
    blacklisted_band = BandName.query.filter_by(id=band_id).first()
    flash(str(blacklisted_band.band_name) + ' has had its blacklist status toggled.')
    blacklisted_band.blacklist(band_id=band_id)
    return redirect(url_for('main.admin_blacklist', ))


@bp.route('/whitelist/<b32:band_id>')
@login_required
def whitelist(band_id):
    whitelisted_band = BandName.query.filter_by(id=band_id).first()
    flash(str(whitelisted_band.band_name) + ' has been manually whitelisted.')
    whitelisted_band.whitelist(band_id=band_id)
    return redirect(url_for('main.admin_blacklist', ))


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/random', methods=['GET', 'POST'])
def random_band():
    random_band = BandName.query.filter(BandName.blacklisted == False).order_by(func.random()).limit(1)
    return render_template('index.html', title='A Random Band Name!', bands=random_band)


@bp.route('/bands', methods=['GET', 'POST'])
def band_names():
    form = BandNameForm()
    if form.validate_on_submit():
        band = BandName(band_name=form.band_name.data)
        db.session.add(band)
        db.session.commit()
        flash('Thanks for the submission!')
        return redirect('/bands')
    all_bands = BandName.all_bands_submitted
    return render_template('bands/band_names.html', title='Band Names!', form=form, bands=all_bands)

