import os
import requests
import random
import re
import json
from flask import Flask, render_template, url_for, flash, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from flask_behind_proxy import FlaskBehindProxy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from chatgpt import ChatGPT
from trefle_api import Plant_image

app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['WTF_CSRF_ENABLED'] = True
# app.config['SECRET_KEY'] = 'super secret key'
app.config['SECRET_KEY'] = 'sk-QI3n64b9a63da2fa31627'
Session(app)

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

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Plants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plnt_name = db.Column(db.String(20), nullable=False)
    # plant_sciname = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Plants('{self.plant_name}')"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Username does not exist. Create an account')
        

with app.app_context():
    db.create_all()


@app.route("/home", methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        if(request.form.get("search") is not None):
            plant_name = request.form.get("search")
            plant = Plant_image(name=plant_name)
            plant_image = plant.image()
            data = ChatGPT(name=plant_name)
            plant_data = data.info()
            plant_data_dict = json.loads(plant_data)

            dbplant_names = Plants(plnt_name=plant_name, user_id=current_user.id)
            db.session.add(dbplant_names)
            db.session.commit()
            return render_template('info.html', plant_data=plant_data_dict, image=plant_image)
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        login_user(user)
        return redirect(url_for('home_page'))

    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash(f'Welcome Back {form.username.data}!', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', title='Log In', form=form)


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
    
@app.route("/portfolio", methods=['GET', 'POST'])
@login_required
def portfolio():
    # pname = None
    # ppic = None

    if request.method == 'POST':
        newname = request.form.get('rename')
        renamed = Plants(plant_name=newname, user_id=current_user.id)
        db.session.add(renamed)
        db.session.commit()

    if request.method == 'GET':
        delname = request.form.get('delete')
        renamed = Plants(plant_name=delname, user_id=current_user.id)
        db.session.add(renamed)
        db.session.commit()
        # pname = request.form['plant_submit']

        # url = 'https://perenual.com/api/species-list?page=1&key=sk-QI3n64b9a63da2fa31627'
        # response = requests.get(url).json()

        # # Search name in common names for the plant
        # for plant_data in response['data']:
        #     if plant_data['common_name'] == pname:
        #         # ppic = response['data'][0]['default_image']['regular_url']
        #         ppic = plant_data['default_image']['regular_url']
        #         print(ppic)
        #         # plant_names = Plants(plant_name=pname, plant_sciname=plant_data['scientific_name'], user_id=current_user.id)
        #         plant_names = Plants(plant_name=pname, user_id=current_user.id)
        #         db.session.add(plant_names)
        #         db.session.commit()
        #         allplants = Plants.query.filter_by(user_id=current_user.id).all()
        #         return render_template('portfolio.html', subtitle='Plant Portfolio', text='Here are all your Plant Children!', ppic = ppic, pname = pname)
        
        # # If name is not in common_names then look for it in other_names
        #     elif plant_data['other_name'] == pname:
        #         ppic = plant_data['default_image']['regular_url']
        #         print(ppic)
        #         # plant_names = Plants(plant_name=pname, plant_sciname=plant_data['scientific_name'], user_id=current_user.id)
        #         plant_names = Plants(plant_name=pname, user_id=current_user.id)
        #         db.session.add(plant_names)
        #         db.session.commit()
        #         allplants = Plants.query.filter_by(user_id=current_user.id).all()
        #         return render_template('portfolio.html', subtitle='Plant Portfolio', text='Here are all your Plant Children!', ppic = ppic, pname = pname)
        #     else:
        #         ppic = "There is no image for this plant!"
        #         return render_template('portfolio.html', subtitle='Plant Portfolio', text='Here are all your Plant Children!', ppic = ppic, pname = pname)
    
    allplants = Plants.query.filter_by(user_id=current_user.id).all()
    return render_template('portfolio.html', subtitle='Plant Portfolio', text='Here are all your Plant Children!', allplants = allplants)

        
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)