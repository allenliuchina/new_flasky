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
