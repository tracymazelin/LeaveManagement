from flask import Blueprint, render_template, flash, request, redirect, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from models import Employee, User, LeaveType, LeaveRequest, Manager
from app import db
from datetime import datetime
from api.controllers import Leave_Types_Api, Leave_Type_Api

import json


main = Blueprint('main', __name__)

#adding keys and values to the context object which is global so it can be accessed by any of the templates
@main.context_processor
def is_employee_admin():
    if current_user.is_authenticated:
        admin = (User.user_is_admin(current_user)).is_admin
    else:
        admin = False
    return dict(user_is_admin=admin)

@main.context_processor
def is_employee_manager():
    if current_user.is_authenticated:
        manager = Manager.user_is_manager(current_user)
        if manager is None:
            manager = True
        else:
            manager = False
    else:
        manager = False
    return dict(user_is_manager=manager)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    data = decode_json(employees.get_employee(current_user.get_id()))
    return render_template('profile.html', employee=data[0])

@main.route('/add_employee')
@login_required
def add_employee():
    return render_template('add_employee.html', managers=Manager.get_all_managers())

@main.route('/add_employee', methods=['POST'])
@login_required
def add_employee_post():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    start_date = datetime.fromisoformat(request.form.get('start_date'))
    is_admin = True if (request.form.get('is_admin')).lower() == 'true' else False 
    manager = request.form.get('manager')
    email = '{}.{}@test.com'.format(first_name.lower(), last_name.lower())

    user = User.query.filter_by(email=email).first() 

    if user: 
        flash('This employee/user already exists.')
        return redirect('add_employee')

    #create new employee with the form data. 
    new_employee = Employee(first_name=first_name, last_name=last_name, start_date=start_date, manager_employee_id=manager, is_admin=is_admin)
    new_user = User(email=email, password=generate_password_hash('test', method='sha256'))
    # add the new employee to the database
    db.session.add(new_employee)
    db.session.add(new_user)
    db.session.commit()
    return render_template('add_employee.html', managers=Manager.get_all_managers())

@main.route('/leave_request')
@login_required
def leave_request():
    return render_template('leave_request.html', types=Leave_Types_Api.get(LeaveType))
    
@main.route('/leave_request', methods=['POST'])
@login_required
def leave_request_post():
    employee = Employee.get_logged_in_employee_id(current_user)
    leave_type = request.form.get('types')
    approval_status = 1
    start_date = datetime.fromisoformat(request.form.get('start_date'))
    end_date = datetime.fromisoformat(request.form.get('end_date'))
    comment = request.form.get('comment')
    leave_request = LeaveRequest(employee_id=employee.employee_id, leave_type_id=leave_type, approval_status_id=approval_status, start_date=start_date, end_date=end_date, comment=comment)
    db.session.add(leave_request)
    db.session.commit()   
    return render_template('leave_request_history.html',  requests=Employee.get_leave_request_history(employee))

@main.route('/leave_request_history')
@login_required
def leave_request_history():
    employee = Employee.get_logged_in_employee_id(current_user)
    return render_template('leave_request_history.html',  requests=Employee.get_leave_request_history(employee))
    
@main.route('/leave_approval')
@login_required
def leave_approval():
    manager = Employee.get_logged_in_employee_id(current_user)
    results =  Employee.get_manager_approval_data(manager)
    print(results[0])
    return render_template('leave_approval.html', requests=results)

@main.route('/approve', methods=['POST'])
@login_required
def approve_post():
    employee = Employee.get_logged_in_employee_id(current_user)
    requestId = request.form.get('decision')
    lr = LeaveRequest.query.filter_by(id=requestId).first() 
    lr.approval_status_id = 2
    db.session.commit()  
    return render_template('leave_approval.html', leave_requests=Employee.get_manager_approval_data(employee))

@main.route('/deny', methods=['POST'])
@login_required
def deny_post():
    employee = Employee.get_logged_in_employee_id(current_user)
    requestId = request.form.get('decision')
    lr = LeaveRequest.query.filter_by(id=requestId).first() 
    lr.approval_status_id = 3
    db.session.commit()  
    return render_template('leave_approval.html', leave_requests=Employee.get_manager_approval_data(employee))