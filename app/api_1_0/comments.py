from . import api
from ..models import Comment, Post, Permission
from flask import jsonify, request, url_for, g
from .decorators import permission_required
from .. import db


@api.route('/comments')
def get_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_comments', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_comments', page=page + 1, _external=True)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total

    })


@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())


@api.route('/posts/<int:id>/comments')
def get_post_comments(id):
    page = request.args.get('page', 1, type=int)
    post = Post.query.get_or_404(id)
    pagination = post.comments.order_by(Comment.timestamp.desc()).paginate(page=page, per_page=5, error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_post_comments', page=page - 1, id=id, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_post_comments', page=page + 1, id=id, _external=True)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total

    })


@api.route('/posts/<int:id>/comments', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_post_comment(id):
    post = Post.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.post = post
    comment.author = g.current_user
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, {'Location': url_for('api.get_comment', id=id, _external=True)}
