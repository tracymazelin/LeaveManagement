from app import db
from flask_login import LoginManager, UserMixin
from datetime import date, datetime

class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	# A constructor function to add a new user
	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = password

class Employee(UserMixin, db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    manager_id = db.Column(db.Integer)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    start_date = db.Column(db.Date, default=date.today())
    is_admin = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref="user")
    leave = db.relationship("LeaveRequest", backref="leave", lazy="dynamic")

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_type.id'))
    approval_status_id = db.Column(db.Integer, db.ForeignKey('approval_status.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    comment = db.Column(db.String(60))
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    employee = db.relationship("Employee", backref="employee")