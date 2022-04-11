from app import db
from flask_login import LoginManager, UserMixin
from datetime import date, datetime

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    
    employee = db.relationship('Employee', backref='user')
    #user.employee will return the employee object
    
    def __repr__(self):
	    return "<User: {} {}>".format(self.user_id, self.email)

    def get_id(self):
        return (self.user_id)

    def user_is_admin(user):
        return (Employee.query.filter_by(user_id=user.user_id).first())

manager_employee = db.Table('manager_employee', 
    db.Column('manager_id', db.Integer, db.ForeignKey('manager.manager_id'), primary_key=True),
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.employee_id'), primary_key=True),
)

class Manager(db.Model):
    manager_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)

    employees = db.relationship('Employee', secondary=manager_employee)

class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True, nullable=False)
    last_name = db.Column(db.String(60), index=True, nullable=False)
    start_date = db.Column(db.Date, default=date.today())
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    

    def get_logged_in_employee_id(user):
        return Employee.query.filter(Employee.employee_id == user.user_id).first()


    
class LeaveType(db.Model):
    leave_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    days_per_year = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)

class ApprovalStatus(db.Model):
    approval_status_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)

class LeaveRequest(db.Model):
    leave_request_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_type.leave_type_id'), nullable=False)
    approval_status_id = db.Column(db.Integer, db.ForeignKey('approval_status.approval_status_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    comment = db.Column(db.String(60), nullable=True)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)

    employee = db.relationship("Employee", backref='leaverequest')
    leavetype = db.relationship("LeaveType", backref='leaverequest')
    status = db.relationship("ApprovalStatus", backref='leaverequest')