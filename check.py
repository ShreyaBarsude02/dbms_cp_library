from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
from datetime import datetime

with open("config.json","r") as c:
    params= json.load(c) ["params"]

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'dbms_cp'


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email_add' in request.form and 'password' in request.form:
        email_add = request.form['email_add']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM accounts WHERE email_add = %s AND password = %s', (email_add, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email_add'] = account['email_add']
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg, params=params)
        else:
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg, params=params)



@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'email_add' in request.form and 'password' in request.form:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email_add = request.form['email_add']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        phone_number = request.form['phone_number']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email_add = %s', (email_add,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_add):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', first_name + last_name):
            msg = 'Name must contain only characters and numbers!'
        else:
            cursor.execute(
                'INSERT INTO accounts (first_name, last_name, email_add, password, repeat_password, date_time, phone_number) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)',
                (first_name, last_name, email_add, password, repeat_password, phone_number,))

            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)



@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html", params=params)
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s',
					(session['id'], ))
		account = cursor.fetchone()
		return render_template("display.html", account=account)
	return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
	msg = ''
	if 'loggedin' in session:
		if request.method == 'POST' and 'first_name' in request.form \
				and 'last_name' in request.form and 'email_add' in request.form \
				and 'password' in request.form and 'repeat_password' in request.form \
				and 'phone_number' in request.form:

			email_add = request.form['email_add']
			first_name = request.form['first_name']
			last_name = request.form['last_name']
			password = request.form['password']
			repeat_password = request.form['repeat_password']
			phone_number = request.form['phone_number']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute(
				'SELECT * FROM accounts WHERE email_add = % s',
					(email_add, ))
			account = cursor.fetchone()
			if account:
				msg = 'Account already exists !'
			elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_add):
				msg = 'Invalid email address !'
			elif not re.match(r'[A-Za-z0-9]+', first_name + last_name):
				msg = 'name must contain only characters and numbers !'
			else:
				cursor.execute('UPDATE accounts SET email_add =% s,\
				first_name =% s, last_name =% s, password =% s, \
				repeat_password =% s, phone_number =% s WHERE id =% s', (
					email_add, first_name, last_name, password,
				repeat_password, phone_number,
				(session['id'], ), ))
				mysql.connection.commit()
				msg = 'You have successfully updated !'
		elif request.method == 'POST':
			msg = 'Please fill out the form !'
		return render_template("update.html", msg=msg)
	return redirect(url_for('login'))

@app.route('/cards')
def cards():
    return render_template('cards.html')

@app.route('/buttons')
def buttons():
    return render_template('buttons.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/AIDS')
def AIDS():
    return render_template('AIDS.html')

@app.route('/Chemical')
def Chemical():
    return render_template('Chemical.html')

@app.route('/Computer')
def Computer():
    return render_template('Computer.html')

@app.route('/CS_AI')
def CS_AI():
    return render_template('CS_AI.html')

@app.route('/CS_AIML')
def CS_AIML():
    return render_template('CS_AIML.html')

@app.route('/ENTC')
def ENTC():
    return render_template('ENTC.html')

@app.route('/Information_tech')
def Information_tech():
    return render_template('Information_tech.html')

@app.route('/Instrumentation')
def Instrumentation():
    return render_template('Instrumentation.html')

@app.route('/Mechanical')
def Mechanical():
    return render_template('Mechanical.html')

@app.route('/add_edit_chem',methods=['GET','POST'])
def add_edit_chem():
    if request.method == "POST":
        details = request.form
        bk_name = details['bookName']
        bk_des = details['bookDesc']
        bk_id = details['bookId']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO bks_chem(bk_name, bk_des, bk_id) VALUES (%s, %s, %s)", (bk_name, bk_des,bk_id))
        mysql.connection.commit()
        cur.close()
        return render_template('index.html',params=params)
    return render_template('add_edit_chem.html')

app.run(host="localhost", debug=True)