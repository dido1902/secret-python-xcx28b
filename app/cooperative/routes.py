from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.cooperative import bp
from app.models.cooperative import Cooperative, CooperativeMember, CooperativeMessage
from app import db
from app.utils.decorators import rate_limit

@bp.route('/cooperatives', methods=['POST'])
@jwt_required()
def create_cooperative():
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
        
    user_id = get_jwt_identity()
    cooperative = Cooperative(
        name=data['name'],
        description=data.get('description', ''),
        admin_id=user_id
    )
    
    db.session.add(cooperative)
    db.session.commit()
    
    # Add creator as first member
    member = CooperativeMember(cooperative_id=cooperative.id, user_id=user_id)
    db.session.add(member)
    db.session.commit()
    
    return jsonify({
        'id': cooperative.id,
        'message': 'Cooperative created successfully'
    }), 201

@bp.route('/cooperatives/<int:id>/join', methods=['POST'])
@jwt_required()
def join_cooperative(id):
    cooperative = Cooperative.query.get_or_404(id)
    user_id = get_jwt_identity()
    
    if CooperativeMember.query.filter_by(
        cooperative_id=id, user_id=user_id).first():
        return jsonify({'error': 'Already a member'}), 409
        
    member = CooperativeMember(cooperative_id=id, user_id=user_id)
    db.session.add(member)
    db.session.commit()
    
    return jsonify({'message': 'Joined cooperative successfully'}), 200

@bp.route('/cooperatives/<int:id>/messages', methods=['POST'])
@jwt_required()
@rate_limit(limit=60, period=3600)  # 60 messages per hour
def send_message(id):
    data = request.get_json()
    
    if not data.get('content'):
        return jsonify({'error': 'Message content is required'}), 400
        
    user_id = get_jwt_identity()
    
    # Verify membership
    if not CooperativeMember.query.filter_by(
        cooperative_id=id, user_id=user_id).first():
        return jsonify({'error': 'Not a member of this cooperative'}), 403
        
    message = CooperativeMessage(
        cooperative_id=id,
        user_id=user_id,
        content=data['content']
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'message': 'Message sent successfully'}), 201

@bp.route('/cooperatives/<int:id>/messages', methods=['GET'])
@jwt_required()
def get_messages(id):
    user_id = get_jwt_identity()
    
    # Verify membership
    if not CooperativeMember.query.filter_by(
        cooperative_id=id, user_id=user_id).first():
        return jsonify({'error': 'Not a member of this cooperative'}), 403
        
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    messages = CooperativeMessage.query.filter_by(cooperative_id=id)\
        .order_by(CooperativeMessage.created_at.desc())\
        .paginate(page=page, per_page=per_page)
    
    return jsonify({
        'messages': [{
            'id': msg.id,
            'content': msg.content,
            'user_id': msg.user_id,
            'created_at': msg.created_at.isoformat()
        } for msg in messages.items],
        'total': messages.total,
        'pages': messages.pages,
        'current_page': messages.page
    }), 200