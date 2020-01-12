from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from app import db, limiter
from app.main.forms import BandNameForm
from app.models import BandName
from app.main import bp
from sqlalchemy.sql.expression import func
from sqlalchemy import exc
from string import capwords


# note: pep8 is grumpy about the boolean equalities; for some reason that's the only way it works. don't touch.

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/random', methods=['GET', 'POST'])
def random_band():
    a_random_band = BandName.query.filter(BandName.blacklisted == False).order_by(func.random()).limit(1)
    return render_template('index.html', title='A Random Band Name!', bands=a_random_band, show_buttons=True)


@bp.route('/top25')
def top25():
    top_scoring_bands = BandName.query.filter(BandName.blacklisted != True).order_by(BandName.votes.desc()).limit(25)
    return render_template('top25.html', title='Top 25 Bands by number of Votes', bands=top_scoring_bands,
                           show_buttons=False)


@bp.route('/upvote/<b32:band_id>')
@limiter.limit('5/second')
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


@bp.route('/bands', methods=['GET', 'POST'])
def band_names():
    form = BandNameForm()
    if form.validate_on_submit():
        band = BandName(band_name=capwords(form.band_name.data))
        try:
            db.session.add(band)
            db.session.commit()
            flash(str(band.band_name) + ' has been added to the database!')
        except exc.IntegrityError as e:
            db.session().rollback()
            flash(str(band.band_name) + ' has already been added to the database!')
        return redirect('/random')
    #    all_bands = BandName.all_bands_submitted
    return render_template('bands/band_names.html', title='Band Names!', form=form)
