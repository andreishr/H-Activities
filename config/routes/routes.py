from flask import Blueprint, request, jsonify, make_response
from ..models import Staff, Patient, Treatment, Treatment_patient
from flask_jwt_extended import (create_access_token, set_access_cookies, jwt_required, 
    get_jwt_identity, unset_jwt_cookies, create_refresh_token, set_refresh_cookies)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from ..init import db

#Create routes blueprint
routes_bp = Blueprint('routes_bp', __name__)
#TODO Create more blueprints and separate routes
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
Management routes -----------------------------------------
'''
'''
Employee management routes
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
        }), 400

    new_emp = Staff(name=emp_name, email=emp_email, password=emp_password, role=emp_role)
    db.session.add(new_emp)
    db.session.commit()
    
    return jsonify(emp_data), 201

@routes_bp.route('/manage/<int:empId>', methods=['PUT'])
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
    


'''
Patient management routes:
'''
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

@routes_bp.route('/patient/<int:patientId>/edit', methods = ['PUT'])
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

    patient.created_at = datetime.now()
    db.session.commit()

    return jsonify({
        'message': 'Credentials modified!'
    }), 200

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

'''
Treatment management routes:
'''
@routes_bp.route('/treatment/add', methods=['POST'])
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
        })
    
    new_treat = Treatment(doctor_id=provided_by, treatment_name=treat_name, description=treat_description)
    db.session.add(new_treat)
    db.session.commit()
    return jsonify(treatment_data), 201  

@routes_bp.route('/treatment/<int:treatId>/edit', methods=['PUT'])
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
            })
        else:
            treatment.doctor_id = data['doc_id']

    db.session.commit()
    return jsonify({
        'message': 'Treatment modified!'
    }), 200

@routes_bp.route('/treatment/<int:treatId>/remove', methods=['DELETE'])
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


'''
Utility routes -----------------------------------------
'''
@routes_bp.route('/give/treatment/<int:patientId>/<int:treatId>', methods=['POST'])
@jwt_required()
def give_treatment(patientId, treatId):
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'doc']:
        return jsonify({
            'message': 'A treatment should be recommended by a doctor.'
        })
    
    data = request.json
    if not data:
        return jsonify({
            'missing': 'Bad Request!'
        }), 400

    employee = Staff.query.get(data['doc_id'])
    if not employee:
        return jsonify({
            'missing': 'Invalid employee ID' 
        }), 400
    if employee.role != 'doc':
        return jsonify({
            'missing': 'Invalid doctor ID' 
        }), 400

    existing_treat = Treatment_patient.query.filter_by(treatment_id=treatId, patient_id=patientId).first()
    if existing_treat is not None:
        return jsonify({
            'message': 'This treatment has been given to this patient.'
        })
    treat_to_patient = Treatment_patient(treatment_id=treatId, patient_id=patientId, assigned_by=employee.staff_id)
    db.session.add(treat_to_patient)
    db.session.commit()
    return jsonify({
        'message': 'Treatment applied!'
    }), 200