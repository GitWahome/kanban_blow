from flask import render_template, url_for, flash, redirect, request,Flask, jsonify
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__,static_folder="./static",template_folder="./templates")
api = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'super secret key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_form'
login_manager.login_message_category = "info"


db = SQLAlchemy(app)
db.create_all()

from kanban import routes