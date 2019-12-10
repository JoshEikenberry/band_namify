from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, PostForm, SearchForm, MessageForm, BandNameForm
from app.models import User, Post, Message, Notification, BandName
from app.translate import translate
from app.main import bp
from sqlalchemy.sql.expression import func, select

@bp.route('/upvote/<band_id>')
def upvote(band_id):
    upvoted_band = BandName.query.filter_by(id=band_id).first()
    flash(str(upvoted_band.band_name) + ' thanks you for your support.')
    upvoted_band.upvote(band_id=band_id)
    return redirect(url_for('main.random_band',))

@bp.route('/report/<band_id>')
def report(band_id):
    reported_band = BandName.query.filter_by(id=band_id).first()
    flash(str(reported_band.band_name) + ' has been reported as being offensive.')
    reported_band.report_band(band_id=band_id)
    return redirect(url_for('main.random_band',))

@bp.route('/blacklist/<band_id>')
def blacklist(band_id):
    blacklisted_band = BandName.query.filter_by(id=band_id).first()
    flash(str(blacklisted_band.band_name) + ' has been blacklisted and will no longer appear on the site.')
    blacklisted_band.blacklist(band_id=band_id)
    return redirect(url_for('main.random_band',))

@bp.route('/whitelist/<band_id>')
def whitelist(band_id):
    whitelisted_band = BandName.query.filter_by(id=band_id).first()
    flash(str(whitelisted_band.band_name) + ' has been whitelisted and will appear on the site.')
    whitelisted_band.whitelist(band_id=band_id)
    return redirect(url_for('main.random_band',))



@bp.route('/random', methods=['GET', 'POST'])
def random_band():
    random_band = BandName.query.order_by(func.random()).limit(1)
    return render_template('index.html', title='A Random Band Name!', bands=random_band)

@bp.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    bands = BandName.query.order_by(BandName.votes.desc()).paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    return render_template('index.html', title='All Band Names Submitted', bands=bands.items)


@bp.route('/', methods=['GET', 'POST'])
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



@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = str(get_locale())



# def index():
#     form = PostForm()
#     if form.validate_on_submit():
#         post = Post(body=form.post.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash(_('Your post is now live!'))
#         return redirect(url_for('main.index'))
#     page = request.args.get('page', 1, type=int)
#     posts = current_user.followed_posts().paginate(
#         page, current_app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('main.index', page=posts.next_num) \
#         if posts.has_next else None
#     prev_url = url_for('main.index', page=posts.prev_num) \
#         if posts.has_prev else None
#     return render_template('index.html', title=_('Home'), form=form,
#                            posts=posts.items, next_url=next_url,
#                            prev_url=prev_url)




@bp.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>/popup')
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title=_('Edit Profile'),
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title=_('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('main.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/export_posts')
@login_required
def export_posts():
    if current_user.get_task_in_progress('export_posts'):
        flash(_('An export task is currently in progress'))
    else:
        current_user.launch_task('export_posts', _('Exporting posts...'))
        db.session.commit()
    return redirect(url_for('main.user', username=current_user.username))


@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
