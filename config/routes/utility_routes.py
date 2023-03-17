from flask import Blueprint, request, jsonify
from ..models import Staff, Patient, Treatment_patient, Assistant_assignment, Assistant_treatment
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..configapp import db

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


@utility_routes_bp.route('/assign', methods=['POST'])
@jwt_required()
def assign_patient():
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
    
    patient_id = data['patient_id']
    assistant_id = data['assistant_id']
    if not patient_id or not assistant_id:
        return jsonify({
            'message': 'Missing Information.'
        }), 400

    patient = Patient.query.get(patient_id)
    if not patient:
        return jsonify({
            'message': 'Invalid patient ID.'
        }), 400
    
    assistant = Staff.query.get(assistant_id)
    if not assistant or assistant.role != 'assist':
        return jsonify({
            'message': 'Invalid assistant ID.'
        }), 400

    already_assigned = Assistant_assignment.query.filter_by(patient_id=patient_id, assistant_id=assistant_id).first()
    if already_assigned:
        return jsonify({
            'message': 'Assignment already exists.'
        })

    new_assignment = Assistant_assignment(patient_id=patient_id, assistant_id=assistant_id)
    db.session.add(new_assignment)
    db.session.commit()
    return jsonify({
        'assistant_id': new_assignment.assistant_id,
        'patient_id': new_assignment.patient_id
    })
    

@utility_routes_bp.route('/tr/applied', methods=['GET', 'POST'])
@jwt_required()
def applied_treatment():
    id = get_jwt_identity()
    staff = Staff.query.filter_by(staff_id=id).first()
    role = staff.role
    if role not in ['gm', 'assist']:
        return jsonify({
            'message': 'Not Authorized!'
        }), 401
    
    if request.method == 'POST':
        if role != 'assist':
            return jsonify({
                'message': 'Treatment should be applied by an assistant'
            })
        data = request.json
        if not data:
            return jsonify({
                'message': 'Bad Request.'
            })
        treatment = data['treat_id']
        if not treatment:
            return jsonify({
                'message': 'Missing Information!'
            })

        treatments = db.session.query(Treatment_patient.treatment_id)\
            .join(Assistant_assignment, Assistant_assignment.patient_id == Treatment_patient.patient_id)\
            .filter(Assistant_assignment.assistant_id == id, Treatment_patient.patient_id == Assistant_assignment.patient_id)\
            .all() 

        treatments_to_be_applied = []
        for treat in treatments:
            treatments_to_be_applied.append(treat.treatment_id)
        
        if treatment not in treatments_to_be_applied:
            return jsonify({
                'message': 'No assigned patients has this treatment prescribed'
            })
        
        treatment_applied = Assistant_treatment(assistant_id=id, treatment_id=treatment)
        db.session.add(treatment_applied)
        db.session.commit()
        return jsonify({
            'treatment_id': treatment,
            'assistant_id': id
        }), 200

    applied_treats = Assistant_treatment.query.all()
    if not applied_treats:
        return jsonify({
            'message': 'No treatments applied by assistants'
        })
    
    list_of_treats = []
    for applied_treat in applied_treats:
        current_treat = {}
        current_treat['assistant_id'] = applied_treat.assistant_id
        current_treat['treatment_id'] = applied_treat.treatment_id
        list_of_treats.append(current_treat)
    
    return jsonify(list_of_treats)
    