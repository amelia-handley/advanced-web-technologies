from flask import Flask, render_template
from flask import request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hannahwashere'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////advanced-web-tech/Coursework2/var/sqlite3.db'
db.init_app(app)

Bootstrap(app)
db = SQLAlchemy(app)
# Classes for Website
# Login Form

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class LogIn(FlaskForm):
    username= StringField('username', validators=[InputRequired(), Length(min=3, max=10)])
    password= PasswordField('password', validators=[InputRequired(), Length(min=5, max=20)])

class Register(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email('Invalid email'), Length(max=30)])
    username= StringField('username', validators=[InputRequired(), Length(min=3, max=10)])
    password= PasswordField('password', validators=[InputRequired(), Length(min=5, max=20)])

#Home Page
@app.route('/')
def root():
    return render_template('home.html'), 200

#Sign up page
@app.route('/create')
def create():
    form = Register()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)

    return render_template('create.html', form=form),200

#Log In page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogIn()
    if form.validate_on_submit():
        return '<h1>' + form.user.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form=form),200

#Game Page
@app.route('/game')
def game():
            return render_template('game.html'),200

#Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/'))

@app.errorhandler(404)
def page_not_found(error):
            return "Couldn't find the page that you have requested", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
