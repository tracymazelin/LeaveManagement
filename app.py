from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from config import Config
import logging
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('faker.factory').setLevel(logging.ERROR)

from models import User, Employee, LeaveRequest, LeaveType, ApprovalStatus, Manager, User

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route("/")
def home():
	
	return redirect(url_for('index'))

@app.route("/index", methods = ["GET", "POST"])
def index():
	return render_template("index.html")

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import main as main_blueprint
app.register_blueprint(main_blueprint)

from api.controllers import api_bp as api_bp
app.register_blueprint(api_bp)

from seed_data import seed as seed

@app.cli.command('db_drop')
def db_create():
    db.drop_all()
    print('Database deleted!')

@app.cli.command('reset_data')
def db_reset():
	db.session.query(ApprovalStatus).delete()
	db.session.query(Employee).delete()
	db.session.query(LeaveType).delete()
	db.session.query(LeaveRequest).delete()
	db.session.query(Manager).delete()
	db.session.query(User).delete()
	db.session.commit()
	print('All data has been reset!')

@app.cli.command('db_create')
def db_create():
	db.init_app(app)
	db.create_all()
	print('Database created!')
	
if __name__=="__main__":
	app.run(debug=True)