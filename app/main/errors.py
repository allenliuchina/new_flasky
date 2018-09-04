from . import main
from flask import render_template, request, jsonify


@main.app_errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': '没有找到'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def interval_server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': '内部错误'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500
