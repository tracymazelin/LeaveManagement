from flask import Blueprint, render_template, flash, request, redirect, jsonify, json
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from models import Employee, User, LeaveType, LeaveRequest, Manager
from app import db
from datetime import date, datetime
import logging
import requests


main = Blueprint('main', __name__)

@main.context_processor
def is_employee_admin():
    data = requests.get('{}/api/employee/{}'.format(base_url(), user_emp_id())).json()
    return dict(user_is_admin=data['is_admin'])

@main.context_processor
def is_employee_manager():
    data = requests.get('{}/api/employee/{}'.format(base_url(), user_emp_id())).json()
    return dict(user_is_manager=data['is_manager'])
   
def base_url():
    url = request.base_url
    return url[:url.rfind('/')]

def user_emp_id():
    return Employee.get_logged_in_employee_id(current_user).employee_id

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    data = requests.get('{}/api/employee/{}'.format(base_url(), user_emp_id())).json()
    return render_template('profile.html', employee=data)

@main.route('/add_employee', methods=['GET'])
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

@main.route('/leave_request', methods=['GET'])
@login_required
def leave_request():
    types = requests.get(base_url()+'/api/leave_types').json()
    return render_template('leave_request.html', types=types)
    
@main.route('/leave_request', methods=['POST'])
@login_required
def leave_request_post():
    leave_type = request.form.get('types')
    approval_status = 1
    start_date = datetime.fromisoformat(request.form.get('start_date'))
    end_date = datetime.fromisoformat(request.form.get('end_date'))
    comment = request.form.get('comment')
    url = base_url()+'/api/leave_requests' 
    headers={"Content-Type":"application/json"}
    r = {"employee": {"id": user_emp_id()},"leave_type": {"id": leave_type},"approval_status": {"id": approval_status},"start_date": start_date.strftime('%Y-%m-%d'),"end_date": end_date.strftime('%Y-%m-%d'),"comment": comment}
    response = requests.post(url, data=json.dumps(r), headers=headers)
    print(response.text)
    data = requests.get('{}/api/employee/{}/leave_requests'.format(base_url(), user_emp_id())).json()
    return render_template('leave_request_history.html', requests=data)
    
@main.route('/leave_request_history', methods=['GET'])
@login_required
def leave_request_history():
    manager = is_employee_manager()
    if manager['user_is_manager']:
        data = requests.get('{}/api/manager/{}/leave_requests'.format(base_url(), user_emp_id())).json()
    else:
        data = requests.get('{}/api/employee/{}/leave_requests'.format(base_url(), user_emp_id())).json()
    return render_template('leave_request_history.html', requests=data)
    
@main.route('/process_requests', methods=['GET'])
@login_required
def process_requests():
    data = requests.get('{}/api/manager/{}/leave_requests'.format(base_url(), user_emp_id())).json()
    return render_template('process.html', requests=data)

@main.route('/approve', methods=['POST'])
@login_required
def approve_post():
    requestId = request.form.get('decision')
    url = '{}/api/leave_request/{}'.format(base_url(), requestId)
    lr = requests.get(url).json()
    lr['approval_status']['id'] = 2
    headers={"Content-Type":"application/json"}
    response = requests.put(url, data=json.dumps(lr), headers=headers)
    data = requests.get('{}/api/manager/{}/leave_requests'.format(base_url(), user_emp_id())).json()
    return render_template('leave_request_history.html', requests=data)

@main.route('/deny', methods=['POST'])
@login_required
def deny_post():
    requestId = request.form.get('decision')
    url = '{}/api/leave_request/{}'.format(base_url(), requestId)
    lr = requests.get(url).json()
    lr['approval_status']['id'] = 3
    headers={"Content-Type":"application/json"}
    response = requests.put(url, data=json.dumps(lr), headers=headers)
    data = requests.get('{}/api/manager/{}/leave_requests'.format(base_url(), user_emp_id())).json()
    return render_template('leave_request_history.html', requests=data)