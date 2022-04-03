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

    def user_is_admin(user):
        return (Employee.query.filter_by(user_id=user.user_id).first())

class Employee(UserMixin, db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), index=True, nullable=False)
    last_name = db.Column(db.String(60), index=True, nullable=False)
    start_date = db.Column(db.Date, default=date.today())
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    deleted_date = db.Column(db.DateTime, index=True, nullable=True, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
