from flask import Blueprint, request, jsonify
from ..models import Staff
from flask_jwt_extended import (create_access_token, set_access_cookies, jwt_required, 
    get_jwt_identity, unset_jwt_cookies, create_refresh_token, set_refresh_cookies)
from werkzeug.security import check_password_hash, generate_password_hash

auth_routes_bp = Blueprint('auth_routes_bp', __name__)

#TEST PURPOSE ONLY TO INSERT
@auth_routes_bp.route('/secretGen', methods = ['POST'])
def secretGen():
    data = request.json
    password = data['password']
    return jsonify({
        'passGen' : generate_password_hash(password)
    }), 200
    

@auth_routes_bp.route('/login', methods = ['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    staff = Staff.query.filter_by(email=email).first()
    
    if not staff:
        return jsonify({
            'message' : 'Wrong email or password'
        }), 401
    if not check_password_hash(staff.password, password):
        return jsonify({
            'message' : 'Wrong email or password'
        }), 401

    access_token = create_access_token(identity=staff.staff_id)
    refresh_token = create_refresh_token(identity=staff.staff_id)
    response = jsonify({
        'message': 'Login successful',
        'access_token': access_token
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    
    return response, 200

@auth_routes_bp.route('/refresh')
@jwt_required(refresh=True)
def refresh():
    id = get_jwt_identity()
    access_token = create_access_token(identity=id)
    response = jsonify({
        'token': access_token
    })
    set_access_cookies(response, access_token, )
    return response


@auth_routes_bp.route('/logout', methods=['DELETE'])
def logout():
    response = jsonify({
        'message': 'Logout successful'
    })
    unset_jwt_cookies(response)
    return response, 200