from flask import Flask, render_template, jsonify, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models import User

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

if __name__=="__main__":
	#db.drop_all()
	db.create_all()
	app.run(debug=True)