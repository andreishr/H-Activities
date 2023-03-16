from config.init import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Staff(db.Model):
    staff_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='n/a')
    patients = relationship("Patient", cascade="all, delete")
    assistants_assign = relationship("Assistant_assignment", cascade="all, delete")
    assistants_treat = relationship("Assistant_treatment", cascade="all, delete")    
    treatments = relationship("Treatment", cascade="all, delete")
    treatments_given = relationship("Treatment_patient", cascade="all, delete")

class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key = True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id', ondelete='CASCADE'))
    name = db.Column(db.String(40), nullable=False)
    age = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    treat_patient = relationship("Treatment_patient", cascade="all, delete")
    assistant_assign = relationship("Assistant_assignment", cascade="all,delete")


class Treatment(db.Model):
    treatment_id = db.Column(db.Integer, primary_key = True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id', ondelete='CASCADE'))
    treatment_name = db.Column(db.Text(), nullable = False)
    description = db.Column(db.Text(), nullable = False)
    treat_patient = relationship("Treatment_patient", cascade="all, delete")
    assistant_treat = relationship("Assistant_treatment", cascade="all,delete")


class Treatment_patient(db.Model):
    applied_treatment = db.Column(db.Integer, primary_key = True)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatment.treatment_id', ondelete='CASCADE'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id', ondelete='CASCADE'), nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey('staff.staff_id', ondelete='CASCADE'), nullable=False)


class Assistant_assignment(db.Model):
    assignment_id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id', ondelete='CASCADE'), nullable=False)
    assistant_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id', ondelete='CASCADE'), nullable=False)


class Assistant_treatment(db.Model):
    applied_id = db.Column(db.Integer, primary_key = True)
    assistant_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id', ondelete='CASCADE'), nullable=False)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatment.treatment_id', ondelete='CASCADE'), nullable=False)



