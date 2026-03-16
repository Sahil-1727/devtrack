from flask import Blueprint, jsonify, request
from app import db, bcrypt
from app.models import User, Application

api = Blueprint('api', __name__, url_prefix='/api')


def get_user_from_token():
    token = request.headers.get('Authorization')
    
    if not token:
        return None
    if token.startswith('Bearer '):
        token = token[7:]
    
    user = User.query.filter_by(api_token=token).first()
   
    return user


@api.route('/health', methods=['GET'])
def health():
    return jsonify({
        'success': True,
        'message': 'DevTrack API is running',
        'version': '1.0'
    })


@api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'success': False, 'message': 'Email and password required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = user.generate_token()
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'username': user.username
        })

    return jsonify({'success': False, 'message': 'Invalid email or password'}), 401


@api.route('/applications', methods=['GET'])
def get_applications():
    user = get_user_from_token()
    if not user:
        return jsonify({'success': False, 'message': 'Invalid or missing token'}), 401

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    status = request.args.get('status', '', type=str)
    per_page = 5

    query = Application.query.filter_by(user_id=user.id)

    if search:
        query = query.filter(
            Application.company.ilike(f'%{search}%') |
            Application.role.ilike(f'%{search}%')
        )

    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(
        Application.date_applied.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    applications = pagination.items

    result = []
    for app in applications:
        result.append({
            'id': app.id,
            'company': app.company,
            'role': app.role,
            'status': app.status,
            'notes': app.notes,
            'date_applied': app.date_applied.strftime('%Y-%m-%d')
        })

    return jsonify({
        'success': True,
        'count': len(result),
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'applications': result
    })

@api.route('/applications', methods=['POST'])
def create_application():
    user = get_user_from_token()
    if not user:
        return jsonify({'success': False, 'message': 'Invalid or missing token'}), 401

    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    if not data.get('company'):
        return jsonify({'success': False, 'message': 'Company is required'}), 400
    if not data.get('role'):
        return jsonify({'success': False, 'message': 'Role is required'}), 400

    application = Application(
        company=data['company'],
        role=data['role'],
        status=data.get('status', 'Applied'),
        notes=data.get('notes', ''),
        user_id=user.id
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Application created',
        'application': {
            'id': application.id,
            'company': application.company,
            'role': application.role,
            'status': application.status
        }
    }), 201


@api.route('/applications/<int:application_id>', methods=['PUT'])
def update_application(application_id):
    user = get_user_from_token()
    if not user:
        return jsonify({'success': False, 'message': 'Invalid or missing token'}), 401

    application = Application.query.get_or_404(application_id)

    if application.user_id != user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400

    if 'company' in data:
        application.company = data['company']
    if 'role' in data:
        application.role = data['role']
    if 'status' in data:
        application.status = data['status']
    if 'notes' in data:
        application.notes = data['notes']

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Application updated',
        'application': {
            'id': application.id,
            'company': application.company,
            'role': application.role,
            'status': application.status
        }
    })


@api.route('/applications/<int:application_id>', methods=['DELETE'])
def delete_application_api(application_id):
    user = get_user_from_token()
    if not user:
        return jsonify({'success': False, 'message': 'Invalid or missing token'}), 401

    application = Application.query.get_or_404(application_id)

    if application.user_id != user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    db.session.delete(application)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Application deleted'})


@api.route('/stats', methods=['GET'])
def get_stats():
    user = get_user_from_token()
    if not user:
        return jsonify({'success': False, 'message': 'Invalid or missing token'}), 401

    applications = Application.query.filter_by(user_id=user.id).all()

    return jsonify({
        'success': True,
        'stats': {
            'total': len(applications),
            'applied': len([a for a in applications if a.status == 'Applied']),
            'interviews': len([a for a in applications if a.status == 'Interview']),
            'offers': len([a for a in applications if a.status == 'Offer']),
            'rejected': len([a for a in applications if a.status == 'Rejected'])
        }
    })