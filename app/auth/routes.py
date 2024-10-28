from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.auth import bp
from app.models.user import User
from app import db
from app.utils.validators import validate_email, validate_password
from app.utils.decorators import rate_limit

@bp.route('/register', methods=['POST'])
@rate_limit(limit=5, period=3600)  # 5 requests per hour
def register():
    data = request.get_json()
    
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
        
    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
        
    if not validate_password(data['password']):
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
        
    user = User(email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
@rate_limit(limit=10, period=300)  # 10 requests per 5 minutes
def login():
    data = request.get_json()
    
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
        
    user = User.query.filter_by(email=data['email']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'role': user.role
        }), 200
        
    return jsonify({'error': 'Invalid credentials'}), 401

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    return jsonify({
        'email': user.email,
        'role': user.role,
        'profile': {
            'age': user.age,
            'monthly_income': user.monthly_income,
            'location': user.location,
            'marital_status': user.marital_status,
            'dependents': user.dependents,
            'employment_status': user.employment_status,
            'years_employed': user.years_employed,
            'sector': user.sector,
            'contract_type': user.contract_type
        }
    }), 200