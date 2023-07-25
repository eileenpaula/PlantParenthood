import os
import requests
import random
import re
import json
from flask import Flask, render_template, url_for, flash, redirect, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_login import login_user
from flask_wtf import FlaskForm
from flask_cors import CORS
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo, InputRequired
from flask_behind_proxy import FlaskBehindProxy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from datetime import datetime
from chatgpt import ChatGPT
from splash_api import Plant_image
from image_rec import Image_Finder


app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'sk-QI3n64b9a63da2fa31627'
app.config['UPLOAD_FOLDER'] = 'static/files'
Session(app)
CORS(app)


# Function to establish database connection
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    plants = db.relationship('Plants', backref='user', lazy=True)
    # plant_sciname = db.relationship('Plants', backref='user', lazy=True)
    def _repr_(self):
        return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Plants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plnt_name = db.Column(db.String(20), nullable=False)
    plnt_care = db.Column(db.JSON, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    # plant_sciname = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def _repr_(self):
        return f"Plants('{self.plnt_name}', '{self.plnt_care}', '{self.date_added}', '{self.image}'')"
        # return f"Plants('{self.plnt_name}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def validate_image(form, field):
    filename = field.data.filename.lower()
    if not filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        field.errors.append('Invalid file format. Only JPG, JPEG, PNG, and GIF images are allowed.')

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired(), validate_image])
    submit = SubmitField("Upload File")

# Function to process the uploaded image
def process_uploaded_image(file):
    # Set the filename to "image" and keep the original file extension
    filename = 'image' + os.path.splitext(file.filename)[1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Create an instance of the Image_Finder class
    image_finder = Image_Finder()
    # Call the image() method to process the uploaded image
    result = image_finder.image()

    return result

with app.app_context():
    db.create_all()

@app.route('/index')
@app.route('/')
def index():
    error = request.args.get('error', None)
    error_type = request.args.get('error_type', None)
    return render_template('index.html', error=error, error_type=error_type)



@app.route("/home", methods=['GET', 'POST'])
def home_page():
    form = UploadFileForm()
    if request.method == 'POST':
        search_query = request.form.get("search")
        if search_query:
            plant_name = search_query
            plant_image, plant_data_dict = Plant_name(plant_name)
            if plant_image != None:
                return render_template('info.html', plant_data=plant_data_dict, image=plant_image)
    if form.validate_on_submit():
        file = form.file.data
        result = process_uploaded_image(file)
        plant_image, plant_data_dict = Plant_name(result)
        if plant_image != None:
            return render_template('info.html', plant_data=plant_data_dict, image=plant_image)
    return render_template('home.html', form=form)


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username is already in the database
        user_by_username = User.query.filter_by(username=username).first()
        if user_by_username:
            return redirect(url_for('index', error='Username already exists!', error_type='signup'))

        # Check if the email is already in the database
        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email:
            return redirect(url_for('index', error='Email already exists!', error_type='signup'))

        # If the username and email are not in the database, insert the new user
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home_page'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match the database
        user = User.query.filter_by(username=username, password=password).first()
        if not user:
            return redirect(url_for('index', error='Invalid username or password!', error_type='login'))

        login_user(user)
        return redirect(url_for('home_page'))



@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        if request.method == 'POST':
            logout_user()
            flash('You have been logged out.', 'success')
            return redirect("/")
        return render_template('logout.html', subtitle='Logout')
    else:
        return redirect("/")

def Plant_name(plant_name):
    data = ChatGPT(name=plant_name)
    if(data.is_plant() == "True"):
        plant = Plant_image(name=plant_name)
        plant_image = plant.image()
        plant_data = data.info()
        plant_data_dict = json.loads(plant_data)
        return plant_image,plant_data_dict
    else:
        return None,None

@app.route("/portfolio", methods=['GET', 'POST'])
@login_required
def portfolio():
    if request.method == 'POST':
        plant_id = request.form.get('plant_id')
        if request.form.get("delete") and plant_id:
            currplant = db.session.get(Plants, plant_id)
            if currplant and (currplant.user_id == current_user.id):
                db.session.delete(currplant)
                db.session.commit()
                flash(f'Plant deleted successfully!', 'success')
            else:
                flash('Plant not found.', 'danger')
    allplants = Plants.query.filter_by(user_id=current_user.id).all()
    print(allplants)
    return render_template('portfolio.html', subtitle='Plant Portfolio', text='Here are all your Plant Children!', allplants=allplants)

# Add plant to portfolio
@app.route('/add_to_portfolio', methods=['POST'])
@login_required
def add_to_portfolio():
    plant_name = request.json.get('plant_name')
    if plant_name:
        plant_image = Plant_image(name=plant_name)
        img = plant_image.image()
        plant_info = ChatGPT(plant_name)
        plant_care = plant_info.careCalendar()
        date = datetime.now()
        new_plant = Plants(plnt_name=plant_name, user_id=current_user.id, plnt_care = plant_care, date_added = date, image = img)
        # new_plant = Plants(plnt_name=plant_name, user_id=current_user.id)
        db.session.add(new_plant)
        db.session.commit()
        flash("Plant added successfully")
        #return {"message": "Plant added successfully!"}, 200
    else:
        return {"message": "Error: No plant name provided."}, 400

@app.route("/rename_plant", methods=['POST'])
@login_required
def rename_plant():
    plant_id = request.form.get('plant_id')
    new_name = request.form.get('new_name')
    if plant_id and new_name:
        plant_to_rename = db.session.get(Plants, plant_id)
        if plant_to_rename and (plant_to_rename.user_id == current_user.id):
            plant_to_rename.plnt_name = new_name
            db.session.commit()
            flash(f'Plant has been renamed to {new_name}!', 'success')
            return jsonify(status='success')
        else:
            flash('Plant not found.', 'danger')
    
    return jsonify(status = 'error')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5001)
