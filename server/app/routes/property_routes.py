from flask import Blueprint, request, jsonify
from app import db
from app.models import Property
from flask_jwt_extended import jwt_required, get_jwt_identity

property_bp = Blueprint('property', __name__)

@property_bp.route('/properties', methods=['GET'])
def get_properties():
    props = Property.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'price': p.price,
        'address': p.address,
        'image_url': p.image_url,
        'user_id': p.user_id
    } for p in props])


@property_bp.route('/properties', methods=['POST'])
@jwt_required()
def create_property():
    data = request.get_json()
    user_id = get_jwt_identity()
    prop = Property(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        address=data['address'],
        image_url=data.get('image_url', ''),
        user_id=user_id
    )
    db.session.add(prop)
    db.session.commit()
    return jsonify(message='Property created'), 201

@property_bp.route('/properties/<int:id>', methods=['GET'])
def get_property(id):
    prop = Property.query.get_or_404(id)
    return jsonify({
        'id': prop.id,
        'title': prop.title,
        'description': prop.description,
        'price': prop.price,
        'address': prop.address,
        'image_url': prop.image_url,
        'user_id': prop.user_id
    })

@property_bp.route('/properties/<int:id>', methods=['PUT'])
@jwt_required()
def update_property(id):
    prop = Property.query.get_or_404(id)
    user_id = get_jwt_identity()
    if prop.user_id != user_id:
        return jsonify(message='Unauthorized'), 403
    data = request.get_json()
    prop.title = data['title']
    prop.description = data['description']
    prop.price = data['price']
    prop.address = data['address']
    prop.image_url = data.get('image_url', prop.image_url)
    db.session.commit()
    return jsonify(message='Property updated')

@property_bp.route('/properties/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_property(id):
    prop = Property.query.get_or_404(id)
    user_id = get_jwt_identity()
    if prop.user_id != user_id:
        return jsonify(message='Unauthorized'), 403
    db.session.delete(prop)
    db.session.commit()
    return jsonify(message='Property deleted')
