from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '123456789'
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)



class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

# Configure Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Create routes for registration and login
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']

        # Check if user already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists.')
            return redirect(url_for('register'))

        # Hash the password before storing it in the database
        password_hash = generate_password_hash(password)

        # Create a new user object and add it to the database
        new_user = User(name=name, surname=surname, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Find the user in the database by email
        user = User.query.filter_by(email=email).first()

        # If the user does not exist or the password is incorrect, redirect to the login page with an error message
        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password')
            return redirect(url_for('login'))

        # If the email and password are valid, log the user in and redirect to the home page
        login_user(user)
        flash('Logged in successfully.')
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



