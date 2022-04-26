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

import models

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route("/")
def home():
	logging.debug("hello")
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

@app.cli.command('db_create')
def db_create():
	db.init_app(app)
	db.create_all()
	print('Database created!')

def register_commands(app):
    """Register CLI commands."""
    app.cli.add_command(seed)

register_commands(app)

if __name__=="__main__":
	app.run(debug=True)