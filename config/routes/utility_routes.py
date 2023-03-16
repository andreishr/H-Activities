from flask import Blueprint, request, jsonify, make_response
from ..models import Staff, Patient, Treatment, Treatment_patient
from flask_jwt_extended import (create_access_token, set_access_cookies, jwt_required, 
    get_jwt_identity, unset_jwt_cookies, create_refresh_token, set_refresh_cookies)
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from ..init import db

utility_routes_bp = Blueprint('utility_routes_bp', __name__)


@utility_routes_bp.route('/give/treatment/<int:patientId>/<int:treatId>', methods=['POST'])
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


@utility_routes_bp.route('/t/applied', methods=['GET'])
@jwt_required()
def get_treat():
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
            'message': 'Bad request!'
        }), 400 

    treat_id = data['treat_id']
    patient_id = data['patient_id']
    if not treat_id or not patient_id:
        return jsonify({
            'message': 'Missing information!'
        }), 400 

    applied_treat = Treatment_patient.query.filter_by(treatment_id=treat_id, patient_id=patient_id).first()
    if not applied_treat:
        return jsonify({
            'message': 'This treatment is not applied to any patient!'
        }), 400

    return jsonify({
        'patient_id': applied_treat.patient_id,
        'treatment_id': applied_treat.treatment_id,
        'given_by_doc_id': applied_treat.assigned_by
    })