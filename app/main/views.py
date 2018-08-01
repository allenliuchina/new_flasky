from .. import db
from flask import render_template, redirect, url_for, session
from . import main

from datetime import datetime

from ..models import User, Role

from .form import NameForm


@main.route('/', methods=['POST', 'GET'])
def index():
    form = NameForm()
    current_time = datetime.utcnow()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', name=session.get('name'), form=form, current_time=current_time)


@main.route('/register', methods=['POST', 'GET'])
def register():
    form = NameForm()
    if form.validate_on_submit() and not User.query.filter_by(username=form.name.data).first():
        user = User(username=form.name.data, role_id=3)
        db.session.add(user)
        return 'ok'
    form.name.data = ''
    return render_template('register.html', form=form)


@main.route('/<name>')
def user_id(name):
    return render_template('user.html', name=name)
