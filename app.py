from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from werkzeug.security import generate_password_hash, check_password_hash

# general flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db' # change this URI as required
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# user database in SQLite
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=True, nullable=False)

    def __repr__(self):
    	return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# forms
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(message="Please enter a valid email."), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message="Please choose a longer password.")])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Log In")

# loading pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/homepage')
def home():
    data = [['Toilet Rolls','Choa Chu Kang CC',130,1.3414251396568244, 103.74075459727348],['Maggie Mee','Choa Chu Kang CC',200],['Hand Sanitiser','Jurong Spring CC',20]]

    return render_template('homepage.html',data = data)

@app.route('/donate')
def don_page():
    return render_template('uploadpage.html')

if __name__ == '__main__':
    app.run()
