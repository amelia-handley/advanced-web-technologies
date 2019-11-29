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
    password = PasswordField('Password', [validators.Length(min=3, max=40)])

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password= sha256_crypt.encrypt(str(form.password.data))

        # Create Cursor
        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))
       
        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You have now created an account', 'success')

        return redirect(url_for('login'))
    return render_template('create.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method== 'POST':
        username= request.form['username']
        password_inputted= request.form['password']

        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username=%s", [username])
        
        # If rows found
        if result > 0:
            data = cur.fetchone()
            password = data['password']
            
            # Compare the password in db to password inputted by user
            if sha256_crypt.verify(password_inputted, password):
                app.logger.info('Correct password')
                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('game'))
            else:
                error='Incorrect Password'
                return render_template('login.html', error=error)

            cur.close()
        else:
            error= 'No user found'
            return render_template('login.html', error=error)

        return redirect(url_for('game'))
    return render_template('login.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have now logged out', 'success')
    return redirect(url_for('home'))

@app.route('/game/start')
def start():
    return render_template('game/chose_start.html')

@app.route('/game/escort')
def escort():
    return render_template('game/chose_escort.html')

@app.route('/game/gun')
def gun():
    return render_template('game/chose_gun.html')

@app.route('/game/coach')
def coach():
    return render_template('game/chose_coach.html')

@app.route('/game/further')
def further():
    return render_template('game/chose_further.html')

@app.route('/game/correct')
def correct():
    return render_template('game/chose_correct.html')

@app.route('/game/incorrect')
def incorrect():
    return render_template('game/chose_incorrect.html')

if __name__ == "__main__":
    app.secret_key='secretshhh'
    app.run(host='0.0.0.0', debug=True)
