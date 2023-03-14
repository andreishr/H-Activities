from flask import Blueprint, request, jsonify, make_response
from ..models import Staff, Patient
from flask_jwt_extended import (create_access_token, set_access_cookies, jwt_required, 
    get_jwt_identity, unset_jwt_cookies, create_refresh_token, set_refresh_cookies)
from werkzeug.security import check_password_hash, generate_password_hash
from ..init import db

#Create routes blueprint
routes_bp = Blueprint('routes_bp', __name__)

'''
Auth routes -----------------------------------------
'''

@routes_bp.route('/login', methods = ['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']
    staff = Staff.query.filter_by(email=email).first()

    if not staff:
        return jsonify({
            'message' : 'Wrong email or password'
        }), 400
    if not check_password_hash(staff.password, password):
        return jsonify({
            'message' : 'Wrong email or password'
        }), 400

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
    access_token = create_access_token(identity=id)
    response = jsonify({
        'token': access_token
    })
    set_access_cookies(response, access_token, )
    return response


@routes_bp.route('/logout', methods=['DELETE'])
def logout():
    response = jsonify({
        'message': 'Logout successful'
    })
    unset_jwt_cookies(response)
    return response, 200



'''
App routes -----------------------------------------
'''

@routes_bp.route('/manage/add', methods=['POST'])
@jwt_required()
def add_employee():
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role

    if role != 'gm':
        return jsonify({
            'message': 'Not authorized!'
        }), 401
    
    emp_data = request.json
    if not emp_data:
        return jsonify({
            'message' : 'Bad request.'
        }), 400
    
    emp_name = emp_data['name']
    emp_email = emp_data['email']
    emp_password = generate_password_hash(emp_data['password'])
    emp_role = emp_data['role']

    if not emp_name or not emp_email or not emp_password or not emp_role:
        return jsonify({
            'message': 'Missing information!'
        }), 400

    if emp_role not in ['doc', 'assist']:
        return jsonify({
            'message': 'Invalid role.'
        }), 

    new_emp = Staff(name=emp_name, email=emp_email, password=emp_password, role=emp_role)
    db.session.add(new_emp)
    db.session.commit()
    
    return jsonify(emp_data), 201

@routes_bp.route('/manage/<int:empId>/remove', methods=['DELETE'])
@jwt_required()
def removeEmployee(empId):
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role != 'gm':
        return jsonify({
            'message': 'Not authorized!'
        }), 401
    else:
        employee = Staff.query.get(empId)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({
            'message': 'Employee removed!'
        })
    

@routes_bp.route('/patient/add', methods=['POST'])
@jwt_required()
def add_patient():
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'doc']:
        return jsonify({
            'message': 'Not authorized!'
        }), 401

    patient_data = request.json
    if not patient_data:
        return jsonify({
            'message' : 'Bad request.'
        }), 400

    patient_name = patient_data['name']
    patient_age = patient_data['age']
    doc_id = patient_data['doc_id']

    if not patient_name or not patient_age or not doc_id:
        return jsonify({
            'message': 'Missing information!'
        }), 401

    appointed_doc = Staff.query.filter_by(staff_id=doc_id).first()
    if not appointed_doc:
        return jsonify({
            'message': 'Provided ID does not belong to any employee.'
        }), 401

    if appointed_doc.role != 'doc':
        return jsonify({
            'message': 'Provided ID does not belong to a doctor.'
        }), 401

    new_patient = Patient(doctor_id=doc_id, name=patient_name, age=patient_age)
    db.session.add(new_patient)
    db.session.commit()

    return jsonify(patient_data), 201

@routes_bp.route('/patient/<int:patientId>/delete', methods=['DELETE'])
@jwt_required()
def remove_patient(patientId):
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'doc']:
        return jsonify({
            'message': 'Not authorized!'
        }), 401
    else:
        patient = Patient.query.get(patientId)
        db.session.delete(patient)
        db.session.commit()
        return jsonify({
            'message': 'Patient removed!'
        })

