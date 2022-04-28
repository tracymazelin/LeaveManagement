# Leave Management #
A python flask web application using PostgreSQL and a Rest-API backend.  This application is hosted Heroku:

[https://tmazelin-leave-management.herokuapp.com/](https://tmazelin-leave-management.herokuapp.com/)

#### Created by: Tracy Mazelin ####

# Main features: #

- Secure user account creation
- Secure user login
- Employees:
    - Submit Leave Requests for manager approval
    - View Leave Request History
- Managers:
    - Approve or deny leave requests
    - View approval history for all employees on team
- Administrators:
    - View all employees
    - Add new employees and assign to managers
    - Edit employees
    - Delete employees

# Credentials

| Type        | Username                  | Password  | Functions                               |
| ----------- | --------------------------|-----------| ----------------------------------------
| Employee    | amanda.robinson@acme.com  | test      | Submit leave request, view history      |
| Manager     | jeremy.ryan@acme.com      | test      | Approve or deny requests, view history  |
| Admin       | kathy.burton@acme.com     | test      | View, add, edit, and delete employees   |


# Installation

The commands below set everything up to run the app locally:

    $ git clone https://github.com/tracymazelin/LeaveManagement
    $ virtualenv venv
    $ . venv/bin/activate
    (venv) pip install -r requirements.txt

Note for Microsoft Windows users: replace the virtual environment activation command above with `venv\Scripts\activate`.

Create a `.env` file with the following

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=9OLWxND4o83 (any random string)
DATABASE_URL=sqlite:///
```  
# To setup the database migrations and seed the tables:

    $ flask db init
    $ flask db migrate
    $ flask db upgrade
    $ flask seed 

# Run the application

    $ flask run

# Utilities

Delete all the tables
    
    $ flask db_drop  

Keep the tables but delete all of the data:

    $ flask db_reset

