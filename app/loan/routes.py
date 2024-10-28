from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.loan import bp
from app.models.user import User
from app.loan.calculator import calculate_loan_eligibility, calculate_monthly_payment
from app.utils.decorators import rate_limit

@bp.route('/calculate-eligibility', methods=['POST'])
@jwt_required()
@rate_limit(limit=10, period=3600)
def calculate_eligibility():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    eligibility = calculate_loan_eligibility(
        age=user.age,
        monthly_income=user.monthly_income,
        employment_status=user.employment_status,
        years_employed=user.years_employed
    )
    
    return jsonify(eligibility), 200

@bp.route('/calculate-payment', methods=['POST'])
@jwt_required()
def calculate_payment():
    data = request.get_json()
    
    if not all(k in data for k in ('loan_amount', 'duration')):
        return jsonify({'error': 'Missing required fields'}), 400
        
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    monthly_payment = calculate_monthly_payment(
        loan_amount=data['loan_amount'],
        duration=data['duration'],
        monthly_income=user.monthly_income
    )
    
    return jsonify({
        'monthly_payment': monthly_payment,
        'total_amount': monthly_payment * data['duration'] * 12
    }), 200