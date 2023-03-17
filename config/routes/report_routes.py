from flask import Blueprint, request, jsonify
from ..models import Staff, Patient, Treatment, Treatment_patient
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..init import db

report_routes_bp = Blueprint('report_routes_bp', __name__)

@report_routes_bp.route('/docs/report', methods=['GET'])
@jwt_required()
def doc_patient():
    id = get_jwt_identity() 
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role != 'gm':
        return jsonify({
            'message': 'Not Authorized!'
        }), 401

    report_result = []
    docs = Staff.query.filter_by(role='doc').all()
    for doc in docs:
        report_dict = {}
        report_dict['doc_id'] = doc.staff_id
        report_dict['doc_name'] = doc.name
        patients = Patient.query.filter_by(doctor_id=doc.staff_id).all()
        patients_list = []
        for patient in patients:
            patient_dict = {}
            patient_dict['patient.id'] = patient.patient_id
            patient_dict['patient_name'] = patient.name
            patients_list.append(patient_dict)
        report_dict['doc_patients'] = patients_list
        report_result.append(report_dict)

    return jsonify(report_result)
   

@report_routes_bp.route('/treat/report', methods=['GET'])
@jwt_required()
def treats_applied():
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'doc']:
        return jsonify({
            'message': 'Not Authorized'
        }), 401
    
    data = request.json
    if not data:
        return jsonify({
            'message': 'Bad request.'
        }), 400
    patient_id = data['patient_id']
    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({
            'message': 'Invalid patient ID'
        })

    treatments = db.session.query(Treatment).join(Treatment_patient, Treatment_patient.treatment_id==Treatment.treatment_id)\
        .filter(Treatment_patient.patient_id==patient_id).all()
    treat_list = []
    for treatment in treatments:
        treat_dict = {}
        treat_dict['treat_id'] = treatment.treatment_id
        treat_dict['treat_name'] = treatment.treatment_name
        treat_dict['treat_desc'] = treatment.description
        treat_list.append(treat_dict)

    treat_report = {}
    treat_report['patient_id'] = patient.patient_id
    treat_report['patient_name'] = patient.name
    treat_report['treats_applied'] = treat_list
    return jsonify(treat_report)