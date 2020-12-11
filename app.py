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
app.secret_key = b'ttRh9-mZp%-&r9/'
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
    confirm = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
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
    data = [['Toilet Rolls','Jurong East Ave 5 Blk 121',130,1.3414251396568244, 103.74075459727348],['Maggie Mee','Whampoa Street 2 Blk 212',140,1.3225507659356324, 103.85295076843762],['Hand Sanitiser','2 First Street',20,1.3129226341821683, 103.92353366040076]]

    return render_template('homepage.html',data = data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run()
