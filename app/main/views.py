from .. import db
from flask import render_template, redirect, url_for, session, abort, flash, request, make_response, current_app, \
    send_from_directory
from . import main
from datetime import datetime
from ..models import User, Role, Permission, Post, Comment
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, CommentForm
from flask_login import current_user, login_required
from ..decorators import permission_required
from flask_sqlalchemy import get_debug_queries
import os
from PIL import Image


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/', methods=['POST', 'GET'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination)


@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30 * 24 * 60 * 60)
    return resp


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        f = form.photo.data
        if f:
            if current_user.file_name:
                try:
                    os.remove(current_app.config['UPLOAD_FOLDER'] + '/photos' + current_user.file_name)
                    os.remove(current_app.config['UPLOAD_FOLDER'] + '/miniphotos' + current_user.file_name)
                except OSError:
                    pass
            filename = str(current_user.id) + '.' + f.filename.split('.')[-1]
            f_1 = Image.open(f)
            f_1.thumbnail((256, 256))
            real_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'photos', filename)
            f_1.save(real_file_path)
            f_2 = Image.open(f)
            f_2.thumbnail((32, 32))
            mini_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'miniphotos', filename)
            f_2.save(mini_file_path)
            current_user.file_name = filename
        db.session.add(current_user)
        flash('You profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/photo/<filename>')
def photo(filename):
    size = request.args.get('size', None, type=int)
    if size == 256:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'] + '/photos', filename)
    elif size == 32:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'] + '/miniphotos', filename)
    else:
        abort(404)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = form.role.data
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.name
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(author=current_user._get_current_object(), post=post, body=form.body.data)
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // 30 + 1
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=30, error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form, comments=comments, pagination=pagination)


@main.route('/edit_post/<int:id>', methods=['POST', 'GET'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user')
        return redirect(url_for('.index'))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user')
        return redirect(url_for('.index'))
    current_user.unfollow(user)
    flash('You are not flollowing %s' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(page, per_page=5, error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', pagination=pagination, follows=follows, user=user, title='Followers of ',
                           endpoint='.followers')


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, per_page=5, error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', pagination=pagination, follows=follows, user=user, title='Followed by ',
                           endpoint='.followed_by')


@main.route('/delete_post/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post is None:
        flash("Invalid post'id")
        return redirect(url_for('.index'))
    if post.author == current_user or current_user.can(Permission.ADMINISTER):
        db.session.delete(post)
        return redirect(url_for('.user', username=current_user.username))
    abort(403)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page=5, error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments, pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/search', methods=['POST'])
def search():
    kw = request.form['search']
    return redirect(url_for('.search_results', kw=kw))


@main.route('/search_results/<kw>')
def search_results(kw):
    results = Post.query.whoosh_search(kw).all()
    return render_template('search.html', posts=results)
