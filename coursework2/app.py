from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)

# Config MySql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'new-password'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# Init MySQL
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=20)])
    email = StringField('Email', [validators.Length(min=4, max=30)])
    password = PasswordField('Password', [validators.Length(min=6, max=50)])

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password= sha256_crypt.encrypt(str(form.password.data))

        # Create Cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", (username, email, password))
        
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You have now created an account and can login', 'success')

        return redirect(url_for('home'))
    return render_template('create.html', form=form)

if __name__ == "__main__":
    app.secret_key='secret1234'
    app.run(host='0.0.0.0', debug=True)
