from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.property import bp
from app.models.property import Property
from app import db
from app.utils.decorators import admin_required

@bp.route('/properties', methods=['GET'])
def get_properties():
    filters = request.args.to_dict()
    query = Property.query
    
    if 'type' in filters:
        query = query.filter(Property.type == filters['type'])
    if 'max_price' in filters:
        query = query.filter(Property.price <= float(filters['max_price']))
    if 'min_surface' in filters:
        query = query.filter(Property.surface >= float(filters['min_surface']))
    if 'location' in filters:
        query = query.filter(Property.location.ilike(f"%{filters['location']}%"))
    if 'status' in filters:
        query = query.filter(Property.status == filters['status'])
    
    properties = query.all()
    return jsonify([{
        'id': p.id,
        'type': p.type,
        'price': p.price,
        'surface': p.surface,
        'location': p.location,
        'status': p.status,
        'sale_type': p.sale_type
    } for p in properties]), 200

@bp.route('/properties', methods=['POST'])
@jwt_required()
@admin_required
def create_property():
    data = request.get_json()
    
    required_fields = ['type', 'price', 'surface', 'location', 'sale_type']
    if not all(k in data for k in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
        
    if data.get('price', 0) > 12000000:
        return jsonify({'error': 'Price exceeds maximum limit'}), 400
    
    property = Property(
        type=data['type'],
        price=data['price'],
        surface=data['surface'],
        location=data['location'],
        sale_type=data['sale_type'],
        status='AVAILABLE'
    )
    
    db.session.add(property)
    db.session.commit()
    
    return jsonify({
        'id': property.id,
        'message': 'Property created successfully'
    }), 201

@bp.route('/properties/<int:id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_property(id):
    property = Property.query.get_or_404(id)
    data = request.get_json()
    
    if 'price' in data:
        if data['price'] > 12000000:
            return jsonify({'error': 'Price exceeds maximum limit'}), 400
        property.price = data['price']
    
    if 'status' in data:
        property.status = data['status']
    
    if 'type' in data:
        property.type = data['type']
    
    if 'surface' in data:
        property.surface = data['surface']
    
    if 'location' in data:
        property.location = data['location']
    
    if 'sale_type' in data:
        property.sale_type = data['sale_type']
    
    db.session.commit()
    
    return jsonify({'message': 'Property updated successfully'}), 200

@bp.route('/properties/<int:id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_property(id):
    property = Property.query.get_or_404(id)
    db.session.delete(property)
    db.session.commit()
    
    return jsonify({'message': 'Property deleted successfully'}), 200