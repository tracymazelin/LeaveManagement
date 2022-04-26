from models import User, Employee, Manager, LeaveRequest, LeaveType, ApprovalStatus
from app import db
from faker import Faker
from datetime import date, datetime
from app import app

fake = Faker()

def add_employees():
    for i in range(1, 12):
        db.session.add(Employee(first_name=fake.first_name(),last_name=fake.last_name()))  
    db.session.commit()
   
    #Admin
    db.session.add(Employee(first_name=fake.first_name(), last_name=fake.last_name(), employee_is_admin=True))
    db.session.commit()

def add_managers():
    db.session.add(Manager(manager_employee_id=1))
    db.session.add(Manager(manager_employee_id=2))
    db.session.commit()

def add_users():
    for i in range(1,13):
        emp=Employee.get_employee_by_id(i)
        user = User(
           email=emp.first_name.lower()+"."+emp.last_name.lower()+"@acme.com",
           password="sha256$ZZfS9TPIqBrlNjmb$90ee9af3cbc6db6a06e9aa769efbc9fe24dbabfb9d68ad763150011a246ad549"
        )
        db.session.add(user)
    db.session.commit()

def assign_managers():
    for i in range(1,7):
        emp = Employee.query.get(i)
        emp.manager_id = 1
    db.session.commit()

    for i in range(7,13):
        emp = Employee.query.get(i)
        emp.manager_id=2
    db.session.commit()

    for i in range(1,3):
        emp = Employee.query.get(i)
        emp.employee_is_manager=True
    db.session.commit()


def assign_users():
    for i in range(1,13):
        emp = Employee.query.get(i)
        emp.user_id = i
    db.session.commit()
  
def add_approval_statuses():
    approval_statuses = ["Pending", "Approved", "Denied"]
    for status in approval_statuses:
        approval_status = ApprovalStatus(
            name=status
        )
        db.session.add(approval_status)
    db.session.commit()

def add_leave_types():
    db.session.add(LeaveType(name="Vacation",days_per_year=20))
    db.session.add(LeaveType(name="Sick",days_per_year=5))
    db.session.add(LeaveType(name="Bereavement",days_per_year=3))
    db.session.add(LeaveType(name="Jury Duty",days_per_year=5))
    db.session.commit()

def add_leave_requests():
    db.session.add(LeaveRequest(employee_id=3, leave_type_id=1, approval_status_id=1, start_date=datetime(2022, 5, 3), end_date=datetime(2022, 5, 5), comment='Need to take the day off'))
    db.session.add(LeaveRequest(employee_id=3, leave_type_id=2, approval_status_id=1, start_date=datetime(2022, 5, 25), end_date=datetime(2022, 5, 26), comment='Dr appointment'))
    db.session.add(LeaveRequest(employee_id=3, leave_type_id=3, approval_status_id=1, start_date=datetime(2022, 6, 27), end_date=datetime(2022, 4, 27), comment='Funeral'))
    db.session.add(LeaveRequest(employee_id=8, leave_type_id=4, approval_status_id=1, start_date=datetime(2022, 5, 9), end_date=datetime(2022, 5, 10), comment='1 day jury duty'))
    db.session.add(LeaveRequest(employee_id=8, leave_type_id=2, approval_status_id=1, start_date=datetime(2022, 6, 6), end_date=datetime(2022, 6, 10), comment='Family vacation'))
    db.session.add(LeaveRequest(employee_id=8, leave_type_id=2, approval_status_id=1, start_date=datetime(2022, 6, 20), end_date=datetime(2022, 6, 22), comment='Surgery'))
    db.session.commit()

@app.cli.command('seed')  
def seed():
    add_employees()
    add_managers()
    add_users()
    assign_managers()
    assign_users()
    add_approval_statuses()
    add_leave_types()
    add_leave_requests()