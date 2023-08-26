from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
import mysql.connector
from werkzeug.utils import secure_filename
import os

with open("config.json","r") as c:
    params= json.load(c) ["params"]

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'samarth1' # enter password here
app.config['MYSQL_DB'] = 'dbms_cp'
app.config['UPLOAD_FOLDER'] = params['upload_location']


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
            flash('Invalid email or password.')
    return render_template('login.html', params=params)



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
            msg = 'You have successfully registered! Go to login'

    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)



@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("index.html", params=params)
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
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bks_chem")
    data = cur.fetchall()
    return render_template('Chemical.html',data=data)

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

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == "POST":
        details = request.form
        bk_name = details['bookName']
        bk_des = details['bookDesc']
        bk_id = details['bookId']
        
        if 'chem' in session and session['chem']:
            if 'file' in request.files:
                file = request.files['file']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO bks_chem(bk_name, bk_des, bk_id, file_path) VALUES (%s, %s, %s, %s)", (bk_name, bk_des, bk_id, file_path))
                    mysql.connection.commit()
                    cur.close()
                    session['chem'] = False

        elif 'com' in session and session['com']:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO bks_com(bk_name, bk_des, bk_id) VALUES (%s, %s, %s)", (bk_name, bk_des, bk_id))
            mysql.connection.commit()
            cur.close()
            session['com'] = False

        elif 'it' in \
                session and session['it']:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO bks_it(bk_name, bk_des, bk_id) VALUES (%s, %s, %s)", (bk_name, bk_des, bk_id))
            mysql.connection.commit()
            cur.close()
            session['it'] = False

        elif 'instru' in session and session['instru']:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO bks_instru(bk_name, bk_des, bk_id) VALUES (%s, %s, %s)", (bk_name, bk_des, bk_id))
            mysql.connection.commit()
            cur.close()
            session['instru'] = False

        elif 'mech' in session and session['mech']:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO bks_mech(bk_name, bk_des, bk_id) VALUES (%s, %s, %s)", (bk_name, bk_des, bk_id))
            mysql.connection.commit()
            cur.close()
            session['mech'] = False

        elif 'entc' in session and session['entc']:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO bks_entc(bk_name, bk_des, bk_id) VALUES (%s, %s, %s)", (bk_name, bk_des, bk_id))
            mysql.connection.commit()
            cur.close()
            session['entc'] = False

        elif 'aids' in session and session['aids']:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO bks_aids(bk_name, bk_des, bk_id) VALUES (%s, %s, %s)", (bk_name, bk_des, bk_id))
            mysql.connection.commit()
            cur.close()
            session['aids'] = False

        elif 'csai' in session and session['csai']:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO bks_csai(bk_name, bk_des, bk_id) VALUES (%s, %s, %s)", (bk_name, bk_des, bk_id))
            mysql.connection.commit()
            cur.close()
            session['csai'] = False

        elif 'csaiml' in session and session['csaiml']:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO bks_csaiml(bk_name, bk_des, bk_id) VALUES (%s, %s, %s)", (bk_name, bk_des, bk_id))
            mysql.connection.commit()
            cur.close()
            session['csaiml'] = False

        return render_template('add_book.html')
    
    return render_template('add_book.html')

@app.route('/edit_book')
def eb():
    return render_template("edit_books.html")

@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if "user" in session and session['user'] == params['admin_user']:
        if 'add' in session and session['add']:
             session.pop('add')
             return render_template("add_book.html")
        elif 'edit' in session and session['edit']:
             session.pop('edit')
             return redirect("/edit_book")

    if request.method == "POST":
        username = request.form.get("username")
        userpass = request.form.get("password")
        if username == params['admin_user'] and userpass == params['admin_password']:
            # set the session variable
            session['user'] = username
            if 'add' in session and session['add']:
                session.pop('add')
                return render_template("add_book.html")
            elif 'edit' in session and session['edit']:
                session.pop('edit')
                return render_template("edit_books.html")
    else:
        flash("Incorrect username or password")
        return render_template("admin_login.html")
    return render_template("admin_login.html")

@app.route('/admin_logout')
def admin_logout():
    session.pop('user')
    return redirect('/index')

@app.route('/add_chem')
def add_chem():
     session['chem'] = True
     session['add'] = True
     return render_template('admin_login.html')
     
@app.route('/add_com')
def add_com():
     session['com'] = True
     return render_template('admin_login.html')

@app.route('/add_it')
def add_it():
     session['it'] = True
     return render_template('admin_login.html')

@app.route('/add_instru')
def add_instru():
     session['instru'] = True
     return render_template('admin_login.html')

@app.route('/add_mech')
def add_mech():
     session['mech'] = True
     return render_template('admin_login.html')

@app.route('/add_entc')
def add_entc():
     session['entc'] = True
     return render_template('admin_login.html')

@app.route('/add_aids')
def add_aids():
     session['aids'] = True
     return render_template('admin_login.html')

@app.route('/add_csai')
def add_csai():
     session['csai'] = True
     return render_template('admin_login.html')

@app.route('/add_csaiml')
def add_csaiml():
     session['csaiml'] = True
     return render_template('admin_login.html')

@app.route('/edit_books')
def edit_books():
    # return render_template('edit.html',  params=params)
    session['edit'] = True
    return render_template('admin_login.html')

@app.route('/edit_chem')
def edit_chem():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bks_chem")
    user = cur.fetchall()
    return render_template('edit_chem.html', user=user)

@app.route("/edit_in_bk_chem/<int:sr_no>", methods=["GET", "POST"])
def edit_in_chem(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bks_chem WHERE sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        query = "UPDATE bks_chem SET bk_name = %s, bk_des = %s, bk_id=%s WHERE sr_no = %s"
        values = (bk_name, bk_des, bk_id,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect("/edit_chem")
    else:
        return render_template("edit.html", book_data=book_data)

@app.route('/edit_comp')
def edit_comp():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bks_com")
    user = cur.fetchall()
    return render_template('edit_comp.html', user=user)

@app.route("/edit_in_bk_comp/<int:sr_no>", methods=["GET", "POST"])
def edit_in_comp(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bks_com WHERE sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        query = "UPDATE bks_com SET bk_name = %s, bk_des = %s, bk_id=%s WHERE sr_no = %s"
        values = (bk_name, bk_des, bk_id,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect("/edit_comp")
    else:
        return render_template("edit.html", book_data=book_data)

@app.route('/edit_it')
def edit_it():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bks_it")
    user = cur.fetchall()
    return render_template('edit_it.html', user=user)

@app.route("/edit_in_bk_it/<int:sr_no>", methods=["GET", "POST"])
def edit_in_it(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bks_it it WHERE sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        query = "UPDATE bks_it SET bk_name = %s, bk_des = %s, bk_id=%s WHERE sr_no = %s"
        values = (bk_name, bk_des, bk_id,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect("/edit_it")
    else:
        return render_template("edit.html", book_data=book_data)

@app.route('/edit_instru')
def edit_instru():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bks_instru")
    user = cur.fetchall()
    return render_template('edit_instru.html', user=user)

@app.route("/edit_in_bk_instru/<int:sr_no>", methods=["GET", "POST"])
def edit_in_instru(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bks_instru it WHERE sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        query = "UPDATE bks_instru SET bk_name = %s, bk_des = %s, bk_id=%s WHERE sr_no = %s"
        values = (bk_name, bk_des, bk_id,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect("/edit_instru")
    else:
        return render_template("edit.html", book_data=book_data)

@app.route('/edit_mech')
def edit_mech():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bks_mech")
    user = cur.fetchall()
    return render_template('edit_mech.html', user=user)

@app.route("/edit_in_bk_mech/<int:sr_no>", methods=["GET", "POST"])
def edit_in_mech(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bks_mech it WHERE sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        query = "UPDATE bks_mech SET bk_name = %s, bk_des = %s, bk_id=%s WHERE sr_no = %s"
        values = (bk_name, bk_des, bk_id,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect("/edit_mech")
    else:
        return render_template("edit.html", book_data=book_data)

@app.route('/edit_entc')
def edit_entc():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bks_entc")
    user = cur.fetchall()
    return render_template('edit_entc.html', user=user)

@app.route("/edit_in_bk_entc/<int:sr_no>", methods=["GET", "POST"])
def edit_in_entc(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bks_entc it WHERE sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        query = "UPDATE bks_entc SET bk_name = %s, bk_des = %s, bk_id=%s WHERE sr_no = %s"
        values = (bk_name, bk_des, bk_id,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect("/edit_entc")
    else:
        return render_template("edit.html", book_data=book_data)

@app.route('/edit_aids')
def edit_aids():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bks_aids")
    user = cur.fetchall()
    return render_template('edit_aids.html', user=user)

@app.route("/edit_in_bk_aids/<int:sr_no>", methods=["GET", "POST"])
def edit_in_aids(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bks_aids it WHERE sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        query = "UPDATE bks_aids SET bk_name = %s, bk_des = %s, bk_id=%s WHERE sr_no = %s"
        values = (bk_name, bk_des, bk_id,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect("/edit_aids")
    else:
        return render_template("edit.html", book_data=book_data)

@app.route('/edit_csai')
def edit_csai():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bks_csai")
    user = cur.fetchall()
    return render_template('edit_csai.html', user=user)

@app.route("/edit_in_bk_csai/<int:sr_no>", methods=["GET", "POST"])
def edit_in_csai(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bks_csai it WHERE sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        query = "UPDATE bks_csai SET bk_name = %s, bk_des = %s, bk_id=%s WHERE sr_no = %s"
        values = (bk_name, bk_des, bk_id,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect("/edit_csai")
    else:
        return render_template("edit.html", book_data=book_data)

@app.route('/edit_csaiml')
def edit_csaiml():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM bks_csaiml")
    user = cur.fetchall()
    return render_template('edit_csaiml.html', user=user)

@app.route("/edit_in_bk_csaiml/<int:sr_no>", methods=["GET", "POST"])
def edit_in_csaiml(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bks_csaiml it WHERE sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        query = "UPDATE bks_csaiml SET bk_name = %s, bk_des = %s, bk_id=%s WHERE sr_no = %s"
        values = (bk_name, bk_des, bk_id,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        return redirect("/edit_csaiml")
    else:
        return render_template("edit.html", book_data=book_data)
    
@app.route("/editBack")
def editBack():
    return redirect("/edit_book")


app.run(host="localhost", debug=True)