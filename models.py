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
    
    def __repr__(self):
	    return "<User: {} {}>".format(self.user_id, self.email)

    def get_id(self):
        return (self.user_id)

    def user_is_admin(user):
        return (Employee.query.filter_by(user_id=user.user_id).first())
    
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
    manager_employee_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'), nullable=True)
    
    manager = db.relationship("Employee", foreign_keys='Employee.manager_employee_id')
   
    def get_logged_in_employee_id(user):
        return Employee.query.filter(Employee.employee_id == user.user_id).first()
    
    def get_employee_by_id(id):
        return Employee.query.get(id)
    
    def get_leave_request_history(employee):
        return LeaveRequest.query.filter(LeaveRequest.employee_id == employee.employee_id).all()

    def get_manager_approval_data(manager):

        data = LeaveRequest.query\
                .join(Employee, LeaveRequest.employee_id == Employee.employee_id)\
                .join(LeaveType, LeaveRequest.leave_type_id == LeaveType.leave_type_id)\
                .join(ApprovalStatus, LeaveRequest.approval_status_id == ApprovalStatus.approval_status_id)\
                .add_columns(Employee.first_name, Employee.last_name, LeaveType.name, LeaveRequest.start_date, LeaveRequest.end_date, ApprovalStatus.name)\
                .filter(Employee.manager_employee_id == manager.employee_id).all()
        
        # data = db.session.query(LeaveRequest, Employee).filter(
        #     LeaveRequest.employee_id == Employee.employee_id,
        #     Employee.manager_employee_id == manager.employee_id
        # ).all()
        #data = Employee.manager_employee_id == manager.employee_id
        print(data)
        return data
    
    def to_dict(self):
        data = {
            'id': self.employee_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_admin': self.is_admin,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'is_manager': True if self.manager_employee_id == None else False,
            'manager': {
                'id': self.manager_employee_id,
                'manager_first_name': None,
                'manager_last_name': None
            }
        }
        return data
    
    def to_collection_dict():
        data = {
            'employees': [item.to_dict() for item in Employee.query.all()]
        }
        return data
    
class LeaveType(db.Model):
    leave_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    days_per_year = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)

    def to_dict(self):
        data = {
            'id': self.leave_type_id,
            'name': self.name,
        }
        return data

    def to_collection_dict():
        data = {
            'leave_types': [item.to_dict() for item in LeaveType.query.all()]
        }
        return data


class ApprovalStatus(db.Model):
    approval_status_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)

    def to_dict(self):
        data = {
            'id': self.approval_status_id,
            'name': self.name,
        }
        return data

    def to_collection_dict():
        data = {
            'leave_types': [item.to_dict() for item in ApprovalStatus.query.all()]
        }
        return data

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
    types = db.relationship("LeaveType", backref='leaverequest')
    status = db.relationship("ApprovalStatus", backref='leaverequest')

    def to_dict(self):
        data = {
            'id': self.leave_request_id,
            'employee': {
                'id': self.employee_id,
                'first_name': self.leaverequest.employee.first_name
            },
            'leave_type': {
                'id': None,
                'name': None
            },
            'approval_status': {
                'id': None,
                'name': None
            },
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d'),
            'comment': self.comment,
            'submitted_date': self.created_date.strftime('%Y-%m-%d')
            
        }
        return data

    def to_collection_dict():
        data = {
            'leave_requests': [item.to_dict() for item in LeaveRequest.query.all()]
        }
        return data

class Manager():
    def user_is_manager(user):
        return (Employee.query.filter_by(user_id=user.user_id).first()).manager_employee_id
    
    def get_manager_details(user):
        pass
       

    def get_all_managers():
        return Employee.query.filter(Employee.manager_employee_id == None).all()