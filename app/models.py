from app import db
from flask_login import LoginManager, UserMixin
from datetime import date, datetime
from flask_restful import Resource, Api, abort, reqparse

class User(UserMixin, db.Model):    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    
    employee = db.relationship('Employee', backref='user', lazy='dynamic')
    
    def __repr__(self):
	    return "<User: {} {}>".format(self.user_id, self.email)

    def get_id(self):
        return (self.user_id)

    def user_is_admin(user):
        return (Employee.query.filter_by(user_id=user.user_id).first())
    
    def get_employee_id(user_id):
        return (Employee.query.filter_by(user_id=user_id).first()).employee_id

class Manager(db.Model):    
    manager_id = db.Column(db.Integer, primary_key=True)
    manager_employee_id = db.Column(db.Integer)

    def user_is_manager(user):
        return (Employee.query.filter_by(user_id=user.user_id).first()).manager_employee_id
    

    def get_all_managers():
        return Employee.query.filter(Employee.manager_employee_id == None).all()
   
class Employee(db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'), nullable=True)
    first_name = db.Column(db.String(60), index=True, nullable=False)
    last_name = db.Column(db.String(60), index=True, nullable=False)
    start_date = db.Column(db.Date, default=date.today())
    employee_is_admin = db.Column(db.Boolean, default=False, nullable=False)
    employee_is_manager = db.Column(db.Boolean, default=False, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
  
    def get_logged_in_employee_id(user):
        return Employee.query.filter_by(user_id=user.user_id).first()
    
    def get_employee_by_id(id):
        return Employee.query.get(id)
    
  
    def get_manager_name_by_id(self, id):
        name = None
        emp_id = int(id) if id else None
        emp = Employee.query.get(emp_id)
        if (type(emp_id) is int):
            name = "{} {}".format(emp.first_name, emp.last_name)
        return name 
       
    def serialize(self):
        return {
            'id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.employee_is_admin,
            'is_manager': self.employee_is_manager,
            'manager': {
                'id': self.manager_id,
                'name': self.get_manager_name_by_id(self.manager_id)
                
            },
            'user_id': self.user_id,
            'start_date': self.start_date.strftime('%Y-%m-%d')  
        }

employee_parser = reqparse.RequestParser(bundle_errors=True)
employee_parser.add_argument('first_name', required=True, help="first name is a required parameter!")
employee_parser.add_argument('last_name', required=True, help="last name is a required parameter!")
employee_parser.add_argument('is_admin', required=True, type=bool, help="is_admin is a required parameter!")
employee_parser.add_argument('is_manager', required=True, type=bool, help="is_manager is a required parameter!")
employee_parser.add_argument('manager', type=dict)
employee_parser.add_argument('start_date', required=True, help="start_date is a required parameter!")
employee_parser.add_argument('user_id')

manager_parser = reqparse.RequestParser(bundle_errors=True)
manager_parser.add_argument('id', type=dict, location=('manager',))
manager_parser = manager_parser.parse_args(req=employee_parser)

class LeaveType(db.Model):
    leave_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    days_per_year = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)

    def serialize(self):
        return {
            'id': self.leave_type_id,
            'name': self.name,
            'days_per_year': self.days_per_year
        }
    
leave_type_parser = reqparse.RequestParser(bundle_errors=True)
leave_type_parser.add_argument('name', required=True, help="name is a required parameter!")
leave_type_parser.add_argument('days_per_year', type=float, required=True, help="days_per_year is a required parameter!")

class ApprovalStatus(db.Model):
    approval_status_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)

    def serialize(self):
        return {
            'id': self.approval_status_id,
            'name': self.name,
        }
       
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
    leaveType = db.relationship("LeaveType", backref='leaverequest')
    status = db.relationship("ApprovalStatus", backref='leaverequest')

    def get_type_name(self, id):
        lt_id = int(id) if id else None
        if (lt_id):
            lt = LeaveType.query.get(lt_id)
            return lt.name
    
    def get_status_name(self, id):
        status_id = int(id) if id else None
        if (status_id):
            status = ApprovalStatus.query.get(status_id)
            return status.name
 
    def serialize(self):
        return {
            'id': self.leave_request_id,
            'employee': {
                'id': self.employee_id,
                'name': '{} {}'.format(Employee.query.get(self.employee_id).first_name, Employee.query.get(self.employee_id).last_name)
            },
            'leave_type': {
                'id': self.leave_type_id,
                'name': self.get_type_name(self.leave_type_id)
            },
            'approval_status': {
                'id': self.approval_status_id,
                'name': self.get_status_name(self.approval_status_id)
            },
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'comment': self.comment,
            'submitted_date': self.created_date.strftime('%Y-%m-%d')    
        }
        
leave_parser = reqparse.RequestParser(bundle_errors=True)
leave_parser.add_argument('start_date', required=True, help="start_date is a required parameter!")
leave_parser.add_argument('end_date', required=True, help="end_date is a required parameter!")
leave_parser.add_argument('comment')
leave_parser.add_argument('employee', type=dict)
leave_parser.add_argument('leave_type', type=dict)
leave_parser.add_argument('approval_status', type=dict)

leave_employee_parser = reqparse.RequestParser(bundle_errors=True)
leave_employee_parser.add_argument('id', type=dict, location=('employee',))
leave_employee_parser = leave_employee_parser.parse_args(req=leave_parser)

leave_type_parser = reqparse.RequestParser(bundle_errors=True)
leave_type_parser.add_argument('id', type=dict, location=('leave_type',))
leave_type_parser = leave_type_parser.parse_args(req=leave_parser)

approval_status_parser = reqparse.RequestParser(bundle_errors=True)
approval_status_parser.add_argument('id', type=dict, location=('leave_type',))
approval_status_parser = approval_status_parser.parse_args(req=leave_parser)