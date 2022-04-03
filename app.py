from flask import Flask, render_template, jsonify, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
	return redirect(url_for('index'))

@app.route("/index", methods = ["GET", "POST"])
def index():
	return render_template("index.html")

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

if __name__=="__main__":
	db.create_all()
	app.run(debug=True)