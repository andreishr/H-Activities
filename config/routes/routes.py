from flask import Blueprint, request, jsonify, make_response
from ..models import Staff, Patient
from flask_jwt_extended import (create_access_token, set_access_cookies, jwt_required, 
    get_jwt_identity, unset_jwt_cookies, create_refresh_token, set_refresh_cookies)
from werkzeug.security import check_password_hash, generate_password_hash
from ..init import db

#Create routes blueprint
routes_bp = Blueprint('routes_bp', __name__)


@routes_bp.route('/login', methods = ['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    staff = Staff.query.filter_by(email=email).first()

    if not staff:
        return jsonify({
            'message' : 'Wrong email or password'
        })
    if not check_password_hash(staff.password, password):
        return jsonify({
            'message' : 'Wrong email or password'
        })

    access_token = create_access_token(identity=staff.staff_id)
    refresh_token = create_refresh_token(identity=staff.staff_id)
    response = jsonify({
        'message': 'Login successful'
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200

@routes_bp.route('/refresh')
@jwt_required(refresh=True)
def refresh():
    id = get_jwt_identity()
    access_token = create_access_token


@routes_bp.route('/logout', methods=['DELETE'])
def logout():
    response = jsonify({
        'message': 'Logout successful'
    })
    unset_jwt_cookies(response)

    return response, 200

@routes_bp.route('/patient/add', methods = ['POST'])
@jwt_required()
def addPatient():
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'doc']:
        return jsonify({
            'message': 'Access forbidden!'
        })

    patient_data = request.json
    patient_name = patient_data['name']
    patient_age = patient_data['age']
    new_patient = Patient(name=patient_name, age=patient_age)
    db.session.add(new_patient)
    db.session.commit()

    return jsonify(patient_data), 201

@routes_bp.route('/patient/<int:patientId>/delete', methods = ['DELETE'])
@jwt_required()
def removePatient(patientId):
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'doc']:
        return jsonify({
            'message': 'Access forbidden!'
        })
    else:
        patient = Patient.query.get(patientId)
        db.session.delete(patient)
        db.session.commit()
        return jsonify({
            'message': 'Patient removed!'
        })