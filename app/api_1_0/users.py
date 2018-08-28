from .authentication import auth
from . import api
from flask import url_for, g, jsonify, request
from ..models import User, Post


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts')
def get_user_posts(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.get_or_404(id)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts', prev=page - 1, id=id, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', next=page + 1, id=id, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<int:id>/timeline')
def get_user_followed_posts(id):
    page = request.args.get('page', 1, type=int)
    user = User.query.get_or_404(id)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts', prev=page - 1, id=id, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts', next=page + 1, id=id, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
