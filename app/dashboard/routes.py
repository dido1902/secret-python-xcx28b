from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.dashboard import bp
from app.models.property import Property
from app.models.loan import Loan
from app.models.user import User
from sqlalchemy import func
from app import db

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    # Property statistics
    total_properties = Property.query.count()
    available_properties = Property.query.filter_by(status='AVAILABLE').count()
    avg_price = db.session.query(func.avg(Property.price)).scalar() or 0
    
    # Loan statistics
    total_loans = Loan.query.count()
    pending_loans = Loan.query.filter_by(status='PENDING').count()
    approved_loans = Loan.query.filter_by(status='APPROVED').count()
    
    # User statistics
    total_users = User.query.count()
    
    return jsonify({
        'properties': {
            'total': total_properties,
            'available': available_properties,
            'average_price': round(avg_price, 2)
        },
        'loans': {
            'total': total_loans,
            'pending': pending_loans,
            'approved': approved_loans,
            'approval_rate': round(approved_loans / total_loans * 100 if total_loans > 0 else 0, 2)
        },
        'users': {
            'total': total_users
        }
    }), 200

@bp.route('/trends', methods=['GET'])
@jwt_required()
def get_trends():
    # Property price trends by type
    price_trends = db.session.query(
        Property.type,
        func.avg(Property.price).label('avg_price'),
        func.count().label('count')
    ).group_by(Property.type).all()
    
    # Loan approval trends
    loan_trends = db.session.query(
        Loan.status,
        func.count().label('count')
    ).group_by(Loan.status).all()
    
    # Location popularity
    location_trends = db.session.query(
        Property.location,
        func.count().label('count')
    ).group_by(Property.location).order_by(func.count().desc()).limit(5).all()
    
    return jsonify({
        'price_trends': [{
            'type': t.type,
            'average_price': round(t.avg_price, 2),
            'count': t.count
        } for t in price_trends],
        'loan_trends': [{
            'status': t.status,
            'count': t.count
        } for t in loan_trends],
        'popular_locations': [{
            'location': t.location,
            'count': t.count
        } for t in location_trends]
    }), 200

@bp.route('/user-stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    user_id = get_jwt_identity()
    
    # User's loan applications
    user_loans = Loan.query.filter_by(user_id=user_id).all()
    
    # Calculate success rate
    total_loans = len(user_loans)
    approved_loans = sum(1 for loan in user_loans if loan.status == 'APPROVED')
    success_rate = round(approved_loans / total_loans * 100 if total_loans > 0 else 0, 2)
    
    return jsonify({
        'loans': {
            'total': total_loans,
            'approved': approved_loans,
            'success_rate': success_rate
        },
        'applications': [{
            'id': loan.id,
            'amount': loan.amount,
            'status': loan.status,
            'created_at': loan.created_at.isoformat()
        } for loan in user_loans]
    }), 200