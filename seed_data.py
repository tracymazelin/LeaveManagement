from models import User, Employee, LeaveRequest, LeaveType, ApprovalStatus
from app import db
from faker import Faker
from datetime import date, datetime
fake = Faker()

def add_employees():
    manager1 = Employee(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        is_admin=False,
        user_id=1,
        manager_employee_id=None
    )
    db.session.add(manager1)
    db.session.commit()

    manager2 = Employee(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        is_admin=False,
        user_id=2,
        manager_employee_id=None
    )
    db.session.add(manager2)
    db.session.commit()

    admin = Employee(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        is_admin=True,
        user_id=3,
        manager_employee_id=1
    )
    db.session.add(admin)
    db.session.commit()
   
    for i in range(4, 5):
        employees1 = Employee(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            is_admin=False,
            user_id=i,
            manager_employee_id=1
        )  
        db.session.add(employees1)
    db.session.commit()
   
    for i in range(5, 7):
        employees2 = Employee(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            is_admin=False,
            user_id=i,
            manager_employee_id=2
        )
        db.session.add(employees2)
    db.session.commit()

def add_users():
    for i in range(1,7):
        emp=Employee.get_employee_by_id(i)
        user = User(
           email=emp.first_name.lower()+"."+emp.last_name.lower()+"@test.com",
           password="sha256$ZZfS9TPIqBrlNjmb$90ee9af3cbc6db6a06e9aa769efbc9fe24dbabfb9d68ad763150011a246ad549"
        )
        db.session.add(user)
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
    db.session.add(LeaveRequest(employee_id=2, leave_type_id=1, approval_status_id=1, start_date=datetime(2022, 4, 3), end_date=datetime(2022, 4, 3), comment='Need to take the day off'))
    db.session.add(LeaveRequest(employee_id=2, leave_type_id=2, approval_status_id=1, start_date=datetime(2022, 5, 5), end_date=datetime(2022, 5, 5), comment='Dr appointment'))
    db.session.add(LeaveRequest(employee_id=3, leave_type_id=3, approval_status_id=1, start_date=datetime(2022, 4, 27), end_date=datetime(2022, 4, 27), comment='Funeral'))
    db.session.add(LeaveRequest(employee_id=4, leave_type_id=4, approval_status_id=1, start_date=datetime(2022, 4, 8), end_date=datetime(2022, 4, 8), comment='1 day jury duty'))
    db.session.add(LeaveRequest(employee_id=5, leave_type_id=2, approval_status_id=1, start_date=datetime(2022, 5, 1), end_date=datetime(2022, 5, 8), comment='Family vacation'))
    db.session.add(LeaveRequest(employee_id=6, leave_type_id=2, approval_status_id=1, start_date=datetime(2022, 4, 6), end_date=datetime(2022, 4, 6), comment='Not feeling good'))
    db.session.commit()
    
def create_data():
    add_employees()
    add_users()
    add_approval_statuses()
    add_leave_types()
    add_leave_requests()