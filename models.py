from app import db
from flask_login import LoginManager, UserMixin
from datetime import date, datetime

class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

	# A constructor function to add a new user
	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = password