from config.init import create_app, db, datetime
app = create_app()

class Staff(db.Model):
    staff_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='n/a')

class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), nullable=False)
    age = db.Column(db.Integer, nullable = False)
    role = db.Column(db.String(20), nullable=False, default='patient')
    created_at = db.Column(db.DateTime, default=datetime.now())
    

class Treatment(db.Model):
    treatment_id = db.Column(db.Integer, primary_key = True)
    treatment_name = db.Column(db.Text(), nullable = False)
    description = db.Column(db.Text(), nullable = False)
    appliedBy = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))


class Relationships(db.Model):
    relation_id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)
    treatment = db.Column(db.Integer, db.ForeignKey('treatment.treatment_id'))


with app.app_context():
    db.create_all()

