from flask_restful import Resource, Api, abort, reqparse
from flask import Blueprint
from app import app
from models import LeaveType, ApprovalStatus, Employee, User, LeaveRequest, leave_type_parser, employee_parser, leave_parser
from app import db
import datetime

api = Api(app)
api_bp = Blueprint('api', __name__)

#LEAVE_TYPE
class Leave_Types_Api(Resource):
    def get(self):
        leave_types = LeaveType.query.all()
        return [LeaveType.serialize(leavetype) for leavetype in leave_types]
    
    def post(self):
        args = parser.parse_args()
        leave_type_record = LeaveType(name=args['name'], days_per_year=args['days_per_year'])
        db.session.add(leave_type_record)
        db.session.commit()
        return LeaveType.serialize(leave_type_record), 201
    
class Leave_Type_Api(Resource):
    def get(self, leave_type_id):
        return LeaveType.serialize(
            LeaveType.query.filter_by(leave_type_id=leave_type_id)
                .first_or_404(description='Leave Type with id={} is not available'.format(leave_type_id)))

    def delete(self, leave_type_id):
        record = LeaveType.query.filter_by(leave_type_id=leave_type_id)\
            .first_or_404(description='Leave Type with id={} is not available'.format(leave_type_id))
        db.session.delete(record)
        db.session.commit()
        return '', 204

    def put(self, leave_type_id):
        args = parser.parse_args()
        record = LeaveType.query.filter_by(leave_type_id=leave_type_id)\
            .first_or_404(description='Leave Type with id={} is not available'.format(leave_type_id))
        record.name = args['name']
        record.days_per_year = args['days_per_year']
        db.session.commit()
        return LeaveType.serialize(record), 201

#APPROVAL_TYPE
class Approval_Statuses_Api(Resource):
    def get(self):
        approval_statuses = ApprovalStatus.query.all()
        return [ApprovalStatus.serialize(approval_status) for approval_status in approval_statuses]

class Approval_Status_Api(Resource):
    def get(self, approval_status_id):
        return ApprovalStatus.serialize(
            ApprovalStatus.query.filter_by(approval_status_id=approval_status_id)
                .first_or_404(description='Approval Status with id={} is not available'.format(approval_status_id)))

#EMPLOYEE
class Employees_Api(Resource):
    def get(self):
        employees = Employee.query.all()
        return [Employee.serialize(employee) for employee in employees]
    
    def post(self):
        args = employee_parser.parse_args()
        employee_record = Employee(first_name=args['first_name'], last_name=args['last_name'], employee_is_admin=args['is_admin'], employee_is_manager=args['is_manager'], manager_id=args['manager']['id'], start_date=datetime.date.fromisoformat(str(args['start_date'])), user_id=args['user_id'])
        db.session.add(employee_record)
        db.session.commit()
        return Employee.serialize(employee_record), 201
    
class Employee_Api(Resource):
    def get(self, employee_id):
        return Employee.serialize(
            Employee.query.filter_by(employee_id=employee_id)
                .first_or_404(description='Employee with id={} is not available'.format(employee_id)))

    def delete(self, employee_id):
        record = Employee.query.filter_by(employee_id=employee_id)\
            .first_or_404(description='Employee with id={} is not available'.format(employee_id))
        user = User.query.get(record.user_id)
        lrs = LeaveRequest.query.filter_by(employee_id=employee_id)
        if lrs:
            for lr in lrs:
                db.session.delete(lr)
        db.session.delete(record)
        db.session.delete(user)
        db.session.commit()
        return '', 204

    def put(self, employee_id):
        args = employee_parser.parse_args()
        record = Employee.query.filter_by(employee_id=employee_id)\
            .first_or_404(description='Employee with id={} is not available'.format(employee_id))
        record.first_name = args['first_name']
        record.last_name = args['last_name']
        record.start_date = datetime.date.fromisoformat(str(args['start_date']))
        record.employee_is_admin = args['is_admin']
        record.employee_is_manager = args['is_manager']
        record.manager_id = args['manager']['id']
        db.session.commit()
        return Employee.serialize(record), 201

#LEAVE_REQUEST
class Leave_Requests_Api(Resource):
    def get(self):
        leave_requests = LeaveRequest.query.all()
        return [LeaveRequest.serialize(leave_request) for leave_request in leave_requests]
    
    def post(self):
        args = leave_parser.parse_args()
        leave_request_record = LeaveRequest(employee_id=args['employee']['id'], leave_type_id=args['leave_type']['id'], \
        approval_status_id=args['approval_status']['id'], start_date=datetime.date.fromisoformat(str(args['start_date'])), end_date=datetime.date.fromisoformat(str(args['end_date'])), comment=args['comment'])
        db.session.add(leave_request_record)
        db.session.commit()
        return LeaveRequest.serialize(leave_request_record), 201
    
class Leave_Request_Api(Resource):
    def get(self, leave_request_id):
        return LeaveRequest.serialize(
            LeaveRequest.query.filter_by(leave_request_id=leave_request_id)
                .first_or_404(description='Leave Request with id={} is not available'.format(leave_request_id)))

    def delete(self, leave_request_id):
        record = LeaveRequest.query.filter_by(leave_request_id=leave_request_id)\
            .first_or_404(description='Leave Request with id={} is not available'.format(leave_request_id))
        db.session.delete(record)
        db.session.commit()
        return '', 204

    def put(self, leave_request_id):
        args = leave_parser.parse_args()
        record = LeaveRequest.query.filter_by(leave_request_id=leave_request_id)\
            .first_or_404(description='Leave Request with id={} is not available'.format(leave_request_id))
        record.start_date = datetime.date.fromisoformat(str(args['start_date']))
        record.end_date = datetime.date.fromisoformat(str(args['end_date']))
        record.comment = args['comment']
        record.employee_id = args['employee']['id']
        record.leave_type_id = args['leave_type']['id']
        record.approval_status_id = args['approval_status']['id']
        db.session.commit()
        return LeaveRequest.serialize(record), 201

#LEAVE_REQUEST_BY_EMPLOYEE
class Employee_Leave_Requests_Api(Resource):
    def get(self, employee_id):
        leave_requests = LeaveRequest.query.filter_by(employee_id=employee_id)
        return [LeaveRequest.serialize(leave_request) for leave_request in leave_requests]
    
    def post(self, employee_id):
        args = leave_parser.parse_args()
        leave_request_record = LeaveRequest(employee_id=employee_id, leave_type_id=args['leave_type']['id'], \
        approval_status_id=args['approval_status']['id'], start_date=datetime.date.fromisoformat(str(args['start_date'])), end_date=datetime.date.fromisoformat(str(args['end_date'])), comment=args['comment'])
        db.session.add(leave_request_record)
        db.session.commit()
        return LeaveRequest.serialize(leave_request_record), 201
    

#MANAGER_EMPLOYEES
class Manager_Employees_Api(Resource):
    def get(self, manager_id):
        employees = Employee.query.filter_by(manager_id=manager_id)
        return [Employee.serialize(emp) for emp in employees]

#MANAGER_LEAVEREQUESTS
class Manager_LeaveRequests_Api(Resource):
    def get(self, manager_id):
        employees = Employee.query.filter_by(manager_id=manager_id)

        emplist = []
        for emp in employees:
            emplist.append(emp.employee_id)
        leave_requests = LeaveRequest.query.filter(LeaveRequest.employee_id.in_(emplist))
        return [LeaveRequest.serialize(req) for req in leave_requests]

#MANAGERS
class Managers_Api(Resource):
    def get(self):
        managers = Employee.query.filter_by(employee_is_manager=True)
        return [Employee.serialize(manager) for manager in managers]


api.add_resource(Leave_Types_Api, '/api/leave_types')
api.add_resource(Leave_Type_Api, '/api/leave_type/<leave_type_id>')
api.add_resource(Approval_Statuses_Api, '/api/approval_statuses')
api.add_resource(Approval_Status_Api, '/api/approval_status/<approval_status_id>')
api.add_resource(Employees_Api, '/api/employees')
api.add_resource(Employee_Api, '/api/employee/<employee_id>')
api.add_resource(Leave_Requests_Api, '/api/leave_requests')
api.add_resource(Leave_Request_Api, '/api/leave_request/<leave_request_id>')
api.add_resource(Employee_Leave_Requests_Api, '/api/employee/<employee_id>/leave_requests')
api.add_resource(Manager_Employees_Api, '/api/manager/<manager_id>/employees')
api.add_resource(Manager_LeaveRequests_Api, '/api/manager/<manager_id>/leave_requests')
api.add_resource(Managers_Api, '/api/managers')