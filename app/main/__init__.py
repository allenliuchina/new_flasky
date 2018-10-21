from flask import Blueprint
from ..models import Permission
from .. import mc
from ..models import User

main = Blueprint('main', __name__)
from . import views, forms, errors, send_log


def generate_greater_users():
    users = User.query.all()
    for user in users:
        mc.get(str(user.id))
    curr = mc.get_stats()[0][1].get('curr_items', '0')
    greater = mc.get('greater_users')
    if int(curr) - 1 > int(greater):
        mc.set('greater_users', int(curr) - 1, time=0)
    return mc.get('greater_users')


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission, curr_users=int(mc.get_stats()[0][1].get('curr_items', 0)) - 1,
                greater_users=int(generate_greater_users()))
