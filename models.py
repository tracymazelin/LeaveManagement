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
    #relationships
    employee = db.relationship('Employee', backref='user', uselist=False)
    #user.employee will return the employee object
    
    def __repr__(self):
	    return "<User: {} {}>".format(self.user_id, self.email)

    def get_id(self):
        return (self.user_id)

    def user_is_admin(user):
        return (Employee.query.filter_by(user_id=user.user_id).first())

class Employee(UserMixin, db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'))
    first_name = db.Column(db.String(60), index=True, nullable=False)
    last_name = db.Column(db.String(60), index=True, nullable=False)
    start_date = db.Column(db.Date, default=date.today())
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    
    #relationships
    #leave_requests = db.relationship('LeaveRequest', backref='employee')
    #manager = db.relationship('Manager', backref='employee')

    def get_logged_in_employee_id(user):
        return Employee.query.filter(Employee.employee_id == user.user_id).first()

class Manager(db.Model):
    manager_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)

    #relationships
    employees = db.relationship('Employee', secondary='manager_employee')

    def get_manager_approval_data(manager):
        return LeaveRequest.query\
        .join(Employee, Employee.employee_id == LeaveRequest.employee_id)\
        .filter(Employee.manager_id == manager.manager_id)\
        .filter(LeaveRequest.approval_status_id == 1).all()
    
    def get_leave_request_history(employee):
        return LeaveRequest.query.filter(LeaveRequest.employee_id == employee.employee_id).all()

    def get_logged_in_employee_id(user):
        return Employee.query.filter(Employee.employee_id == user.user_id).first()
    
    def user_is_manager(user):
        return (Employee.query.filter_by(user_id=user.user_id).first()).manager_id

    def get_all_managers():
        return Employee.query.filter(Employee.manager_id == None).all()

manager_employee = db.Table('manager_employee', 
    db.Column('manager_employee_id', db.Integer, primary_key=True),
    db.Column('manager_id', db.Integer, db.ForeignKey('manager.manager_id'), nullable=True),
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
)

class LeaveRequest(db.Model):
    leave_request_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=False)
    leave_type_id = db.Column(db.Integer, db.ForeignKey('leave_type.leave_type_id'), nullable=False)
    approval_status_id = db.Column(db.Integer, db.ForeignKey('approval_status.approval_status_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    comment = db.Column(db.String(60), nullable=True)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)

    employee = db.relationship("Employee", backref='leaverequest')
    leavetypes = db.relationship("LeaveType", backref='leaverequest')
    statuses = db.relationship("ApprovalStatus", backref='leaverequest')


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