from flask import Blueprint, request, jsonify
from ..models import Staff, Patient, Treatment
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from datetime import datetime
from ..configapp import db

manage_routes_bp = Blueprint('manage_routes_bp', __name__)


@manage_routes_bp.route('/manage/add', methods=['POST'])
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
        }), 400

    new_emp = Staff(name=emp_name, email=emp_email, password=emp_password, role=emp_role)
    db.session.add(new_emp)
    db.session.commit()
    
    return jsonify(emp_data), 201

@manage_routes_bp.route('/manage/<int:empId>', methods=['PUT'])
@jwt_required()
def update_employee(empId):
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role

    if role != 'gm':
        return jsonify({
            'message': 'Not authorized!'
        }), 401

    data = request.json
    if not data:
        return jsonify({
            'message': 'Bad request.'
        }), 400

    employee = Staff.query.get(empId)
    if not employee:
        return jsonify({
            'message': 'Invalid employee ID.'
        }), 400
    if data['name'] != "":
        employee.name = data['name']

    if data['email'] != "":
        employee.email = data['email'] 

    if data['password'] != "":
        employee.password = generate_password_hash(data['password'])
        
    if data['role'] != "":
        if data['role'] not in ['gm', 'doc', 'assist']:
            return jsonify({
                'message': 'Invalid role.'
            }), 400
        else:
            employee.role = data['role']

    db.session.commit()

    return jsonify({
        'message': 'Credentials modified!'
    }), 200

@manage_routes_bp.route('/manage/<int:empId>/remove', methods=['DELETE'])
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
    



'''
Patient management routes:
'''
@manage_routes_bp.route('/patient/add', methods=['POST'])
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
        }), 400

    appointed_doc = Staff.query.filter_by(staff_id=doc_id).first()
    if not appointed_doc:
        return jsonify({
            'message': 'Provided ID does not belong to any employee.'
        }), 400

    if appointed_doc.role != 'doc':
        return jsonify({
            'message': 'Provided ID does not belong to a doctor.'
        }), 400

    new_patient = Patient(doctor_id=doc_id, name=patient_name, age=patient_age)
    db.session.add(new_patient)
    db.session.commit()

    return jsonify(patient_data), 201


@manage_routes_bp.route('/patient/<int:patientId>/edit', methods = ['PUT'])
@jwt_required()
def edit_patient(patientId):
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'doc']:
        return jsonify({
            'message': 'Not authorized!'
        }), 401
    data = request.json
    if not data:
        return jsonify({
            'message': 'Bad Request.'
        }), 400
    patient = Patient.query.get(patientId)
    if not patient:
        return jsonify({
            'message': 'Invalid patient ID.'
        }), 400
    if data['doc_id'] != "":
        appointed_doc = Staff.query.get(data['doc_id'])
        if not appointed_doc:
            return jsonify({
                'message': 'Provided ID does not belong to any employee.'
            }), 400
        if appointed_doc.role != 'doc':
            return jsonify({
                'message': 'Provided ID does not belong to a doctor.'
            }), 400
        else:
            patient.doctor_id = data['doc_id']
    
    if data['name'] != "":
        patient.name = data['name']

    if data['age'] != "":
        patient.age = data['age']

    if data['disease'] != "":
        patient.disease = data['disease']

    if data['details'] != "":
        patient.details = data['details']
    
    patient.created_at = datetime.now()
    db.session.commit()

    return jsonify({
        'message': 'Credentials modified!'
    }), 200


@manage_routes_bp.route('/patient/<int:patientId>/delete', methods=['DELETE'])
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
        }), 204



'''
Treatment management routes:
'''
@manage_routes_bp.route('/treatment/add', methods=['POST'])
@jwt_required()
def add_treatment():
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'doc']:
        return jsonify({
            'message': 'Not authorized!'
        }), 401
    
    treatment_data = request.json
    if not treatment_data:
        return jsonify({
            'message': 'Bad request.'
        }), 400
    treat_name = treatment_data['name']
    treat_description = treatment_data['description']
    provided_by = treatment_data['doc_id']

    if not treat_name or not treat_description or not provided_by:
        return jsonify({
            'message': 'Missing information!'
        }), 400

    provided_staff = Staff.query.get(provided_by)
    if not provided_staff:
        return jsonify({
            'message': 'Invalid employee ID.'
        }), 400
    if provided_staff.role != 'doc':
        return jsonify({
            'message': 'Cannot add a treatment that is not issued by a doctor.'
        }), 401
    
    new_treat = Treatment(doctor_id=provided_by, treatment_name=treat_name, description=treat_description)
    db.session.add(new_treat)
    db.session.commit()
    return jsonify(treatment_data), 201  


@manage_routes_bp.route('/treatment/<int:treatId>/edit', methods=['PUT'])
@jwt_required()
def edit_treatment(treatId):
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'doc']:
        return jsonify({
            'message': 'Not Authorized!'
        }), 401

    data = request.json
    if not data:
        return jsonify({
            'message': 'Bad request.'
        }), 400

    treatment = Treatment.query.get(treatId)
    if not treatment:
        return jsonify({
            'message': 'Invalid treatment ID!'
        }), 400

    if data['name'] != "":
        treatment.treatment_name = data['name']

    if data['description'] != "":
        treatment.description = data['description']

    if data['doc_id'] != "":
        provided_staff = Staff.query.get(data['doc_id'])
        if not provided_staff:
            return jsonify({
            '   message': 'Invalid employee ID.'
            }), 400
        if provided_staff.role != 'doc':
            return jsonify({
                'message': 'Cannot add a treatment that is not issued by a doctor.'
            }), 401
        else:
            treatment.doctor_id = data['doc_id']

    db.session.commit()
    return jsonify({
        'message': 'Treatment modified!'
    }), 200


@manage_routes_bp.route('/treatment/<int:treatId>/remove', methods=['DELETE'])
@jwt_required()
def remove_treatment(treatId):
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'doc']:
        return jsonify({
            'message': 'Not Authorized!'
        }), 401
    treatment = Treatment.query.get(treatId)
    db.session.delete(treatment)
    db.session.commit()

    return jsonify({
        'message': 'Treatment removed!'
    })