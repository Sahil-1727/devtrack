from flask import Blueprint, render_template, jsonify, request

errors = Blueprint('errors', __name__)


def wants_json_response():
    # Check if request wants JSON (API call) or HTML (browser)
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']


@errors.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def forbidden_error(error):
    if wants_json_response():
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'You do not have permission to access this resource'
        }), 403
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def internal_error(error):
    from app import db
    db.session.rollback()
    if wants_json_response():
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500
    return render_template('errors/500.html'), 500