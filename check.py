from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import json
import mysql.connector
from werkzeug.utils import secure_filename
import os
import datetime
import cv2 
from pyzbar.pyzbar import decode
from datetime import timedelta
import calendar

scanning = False

with open("config.json","r") as c:
    params= json.load(c) ["params"]

app = Flask(__name__)

app.secret_key = 'your secret key'


prn1 = None



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sucasa@2021' # enter password here
app.config['MYSQL_DB'] = 'dbms_cp'
app.config['UPLOAD_FOLDER'] = params['upload_location']


mysql = MySQL(app)
count = 0







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
            session['prn'] = account['prn']
            session['email_add'] = account['email_add']
            msg = 'Logged in successfully!'
            current_datetime = datetime.datetime.now()
            currentdate = current_datetime.date()
            session['count'] = count


            # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cur.execute("SELECT * FROM book_issue where count = '1' AND prn = session['prn']" )
            # data = cur.fetchall()



            query = "SELECT * FROM book_issue WHERE count = %s AND prn = %s"
            cursor.execute(query, ('1', session['prn']))
            data = cursor.fetchall()



            
            return render_template('index.html', msg=msg, params=params, currentdate=currentdate, data=data)
        else:
            flash('Invalid email or password.')
    return render_template('login.html', params=params)



@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('prn', None)
	session.pop('username', None)
	return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'email_add' in request.form and 'password' in request.form and 'prn' in request.form:
        # prn = request.form['prn']
        prn = request.form['prn']
        session['prn'] = prn  # Store the prn in the session
        # Other registration logic
        # print("this is ", prn1)
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
                'INSERT INTO accounts ( prn,first_name, last_name, email_add, password, repeat_password, date_time, phone_number) VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s)',
                (prn,first_name, last_name, email_add, password, repeat_password, phone_number))

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
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'AIDS' ")
    data = cur.fetchall()
    return render_template('AIDS.html',data=data)

@app.route('/Chemical')
def Chemical():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'Chemical' ")
    data = cur.fetchall()
    return render_template('Chemical.html',data=data)

@app.route('/Computer')
def Computer():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'Computer'")
    data = cur.fetchall()
    return render_template('Computer.html',data=data)

@app.route('/CS_AI')
def CS_AI():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'CSAI' ")
    data = cur.fetchall()
    return render_template('CS_AI.html',data=data)

@app.route('/CS_AIML')
def CS_AIML():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'CSAIML' ")
    data = cur.fetchall()
    return render_template('CS_AIML.html',data=data)

@app.route('/ENTC')
def ENTC():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'ENTC' ")
    data = cur.fetchall()
    return render_template('ENTC.html',data=data)

@app.route('/Information_tech')
def Information_tech():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'InformationTech'")
    data = cur.fetchall()
    return render_template('Information_tech.html',data=data)

@app.route('/Instrumentation')
def Instrumentation():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'Instrumentation' ")
    data = cur.fetchall()
    return render_template('Instrumentation.html',data=data)

@app.route('/Mechanical')
def Mechanical():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'Mechinacal' ")
    data = cur.fetchall()
    return render_template('Mechanical.html',data=data)




@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == "POST":
        details = request.form
        bk_name = details['bookName']
        bk_des = details['bookDesc']
        bk_id = details['bookId']
        author = details['author']
        dept = session['dept']
        dept_id = session['dept_id']
        
        try:
            if 'file' in request.files:
                
                file = request.files['file']
                if file.filename != '':
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    cur = mysql.connection.cursor()
                    cur.execute("INSERT INTO books(dept_id,dept, bk_id,author,bk_name, bk_des, file_path) VALUES (%s,%s,%s, %s, %s, %s,%s)", (dept_id,dept,bk_id,author,bk_name, bk_des,file_path))
                    mysql.connection.commit()
                    cur.close()
                    
                    return render_template('add_book.html')
        except Exception as e:
            print(e)
            flash("Book ID should be UNIQUE") 
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
    session.pop('dept_id')
    session.pop('dept')
    session.pop('user')
    return redirect('/index')

@app.route('/add_chem')
def add_chem():
     session['dept'] = "Chemical"
     session['dept_id'] = "D1"
    #  session['chem'] = True
     session['add'] = True
     return render_template('admin_login.html')
     
@app.route('/add_com')
def add_com():
     session['dept'] = "Computer"
     session['dept_id'] = "D2"
    #  session['com'] = True
     session['add'] = True
     return render_template('admin_login.html')

@app.route('/add_it')
def add_it():
     session['dept'] = "InformationTech"
     session['dept_id'] = "D7"
    #  session['it'] = True
     session['add'] = True
     return render_template('admin_login.html')

@app.route('/add_instru')
def add_instru():
     session['dept'] = "Instrumentation"
     session['dept_id'] = "D6"
     #  session['instru'] = True
     session['add'] = True
     return render_template('admin_login.html')

@app.route('/add_mech')
def add_mech():
     session['dept'] = "Mechinacal"
     session['dept_id'] = "D8"
    #  session['mech'] = True
     session['add'] = True
     return render_template('admin_login.html')

@app.route('/add_entc')
def add_entc():
     session['dept'] = "ENTC"
     session['dept_id'] = "D5"
    #  session['entc'] = True
     session['add'] = True
     return render_template('admin_login.html')

@app.route('/add_aids')
def add_aids():
     session['dept'] = "AIDS"
     session['dept_id'] = "D0"
    #  session['aids'] = True
     session['add'] = True
     return render_template('admin_login.html')

@app.route('/add_csai')
def add_csai():
     session['dept'] = "CSAI"
     session['dept_id'] = "D3"
    #  session['csai'] = True
     session['add'] = True
     return render_template('admin_login.html')

@app.route('/add_csaiml')
def add_csaiml():
     session['dept'] = "CSAIML"
     session['dept_id'] = "D4"
    #  session['csaiml'] = True
     session['add'] = True
     return render_template('admin_login.html')

@app.route('/edit_books')
def edit_books():
    # return render_template('edit.html',  params=params)
    session['edit'] = True
    return render_template('admin_login.html')

@app.route('/edit_chem')
def edit_chem():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'Chemical' ")
    user = cur.fetchall()
    return render_template('edit_chem.html', user=user)

@app.route("/edit_in_bk_chem/<int:sr_no>", methods=["GET", "POST"])
def edit_in_chem(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books WHERE dept = 'Chemical' AND sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    old_filename = book_data['file_path']# retrieving old img path from db
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        bk_file = request.files["bk_file"]# taking new file path 
        filenaemEdit = secure_filename(bk_file.filename)#securing name of file 
        filepathEdit=os.path.join(app.config['UPLOAD_FOLDER'],filenaemEdit)#joining folder path with filename 
        bk_file.save(filepathEdit)#seving file to staric/img folder
        query = "UPDATE books SET bk_name = %s, bk_des = %s, bk_id=%s, file_path=%s WHERE dept = 'Chemical' AND sr_no = %s"
        values = (bk_name, bk_des, bk_id,filepathEdit,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        os.remove(old_filename)#removing old img from static/img folder
        cursor.close()
        return redirect("/edit_chem")
    else:
        return render_template("edit.html", book_data=book_data ,dep="chem")
    

@app.route('/edit_comp')
def edit_comp():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'Computer'")
    user = cur.fetchall()
    return render_template('edit_comp.html', user=user)

@app.route("/edit_in_bk_comp/<int:sr_no>", methods=["GET", "POST"])
def edit_in_comp(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books WHERE dept = 'Computer' AND sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    old_filename = book_data['file_path']# retrieving old img path from db
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        bk_file = request.files["bk_file"]# taking new file path 
        filenaemEdit = secure_filename(bk_file.filename)#securing name of file 
        filepathEdit=os.path.join(app.config['UPLOAD_FOLDER'],filenaemEdit)#joining folder path with filename 
        bk_file.save(filepathEdit)#seving file to staric/img folder
        query = "UPDATE books SET bk_name = %s, bk_des = %s, bk_id=%s, file_path=%s WHERE dept = 'Computer' AND sr_no = %s"
        values = (bk_name, bk_des, bk_id,filepathEdit,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        os.remove(old_filename)#removing old img from static/img folder
        cursor.close()
        return redirect("/edit_comp")
    else:
        return render_template("edit.html", book_data=book_data , dep = "comp")



@app.route('/edit_it')
def edit_it():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'InformationTech'")
    user = cur.fetchall()
    return render_template('edit_it.html', user=user)

@app.route("/edit_in_bk_it/<int:sr_no>", methods=["GET", "POST"])
def edit_in_it(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books WHERE dept = 'InformationTech' AND sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    old_filename = book_data['file_path']# retrieving old img path from db
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        bk_file = request.files["bk_file"]# taking new file path 
        filenaemEdit = secure_filename(bk_file.filename)#securing name of file 
        filepathEdit=os.path.join(app.config['UPLOAD_FOLDER'],filenaemEdit)#joining folder path with filename 
        bk_file.save(filepathEdit)#seving file to staric/img folder
        query = "UPDATE books SET bk_name = %s, bk_des = %s, bk_id=%s, file_path=%s WHERE dept = 'InformationTech' AND sr_no = %s"
        values = (bk_name, bk_des, bk_id,filepathEdit,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        os.remove(old_filename)#removing old img from static/img folder
        cursor.close()
        return redirect("/edit_it")
    else:
        return render_template("edit.html", book_data=book_data,dep="it")

@app.route('/edit_instru')
def edit_instru():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'Instrumentation'")
    user = cur.fetchall()
    return render_template('edit_instru.html', user=user)

@app.route("/edit_in_bk_instru/<int:sr_no>", methods=["GET", "POST"])
def edit_in_instru(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books WHERE dept = 'Instrumentation' AND sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    old_filename = book_data['file_path']# retrieving old img path from db
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        bk_file = request.files["bk_file"]# taking new file path 
        filenaemEdit = secure_filename(bk_file.filename)#securing name of file 
        filepathEdit=os.path.join(app.config['UPLOAD_FOLDER'],filenaemEdit)#joining folder path with filename 
        bk_file.save(filepathEdit)#seving file to staric/img folder
        query = "UPDATE books SET bk_name = %s, bk_des = %s, bk_id=%s, file_path=%s WHERE dept = 'Instrumentation' AND sr_no = %s"
        values = (bk_name, bk_des, bk_id,filepathEdit,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        os.remove(old_filename)#removing old img from static/img folder
        cursor.close()
        return redirect("/edit_instru")
    else:
        return render_template("edit.html", book_data=book_data,dep="instru")

@app.route('/edit_mech')
def edit_mech():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'Mechinacal'")
    user = cur.fetchall()
    return render_template('edit_mech.html', user=user)

@app.route("/edit_in_bk_mech/<int:sr_no>", methods=["GET", "POST"])
def edit_in_mech(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books WHERE dept = 'Mechinacal' AND sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    old_filename = book_data['file_path']# retrieving old img path from db
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        bk_file = request.files["bk_file"]# taking new file path 
        filenaemEdit = secure_filename(bk_file.filename)#securing name of file 
        filepathEdit=os.path.join(app.config['UPLOAD_FOLDER'],filenaemEdit)#joining folder path with filename 
        bk_file.save(filepathEdit)#seving file to staric/img folder
        query = "UPDATE books SET bk_name = %s, bk_des = %s, bk_id=%s, file_path=%s WHERE dept = 'Mechinacal' AND sr_no = %s"
        values = (bk_name, bk_des, bk_id,filepathEdit,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        os.remove(old_filename)#removing old img from static/img folder
        cursor.close()
        return redirect("/edit_mech")
    else:
        return render_template("edit.html", book_data=book_data, dep="mech")

@app.route('/edit_entc')
def edit_entc():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'ENTC'")
    user = cur.fetchall()
    return render_template('edit_entc.html', user=user)

@app.route("/edit_in_bk_entc/<int:sr_no>", methods=["GET", "POST"])
def edit_in_entc(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books WHERE dept = 'ENTC' AND sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    old_filename = book_data['file_path']# retrieving old img path from db
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        bk_file = request.files["bk_file"]# taking new file path 
        filenaemEdit = secure_filename(bk_file.filename)#securing name of file 
        filepathEdit=os.path.join(app.config['UPLOAD_FOLDER'],filenaemEdit)#joining folder path with filename 
        bk_file.save(filepathEdit)#seving file to staric/img folder
        query = "UPDATE books SET bk_name = %s, bk_des = %s, bk_id=%s, file_path=%s WHERE dept = 'ENTC' AND sr_no = %s"
        values = (bk_name, bk_des, bk_id,filepathEdit,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        os.remove(old_filename)#removing old img from static/img folder
        cursor.close()
        return redirect("/edit_entc")
    else:
        return render_template("edit.html", book_data=book_data, dep="entc")

@app.route('/edit_aids')
def edit_aids():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'AIDS'")
    user = cur.fetchall()
    return render_template('edit_aids.html', user=user)

@app.route("/edit_in_bk_aids/<int:sr_no>", methods=["GET", "POST"])
def edit_in_aids(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books WHERE dept = 'AIDS' AND sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    old_filename = book_data['file_path']# retrieving old img path from db
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        bk_file = request.files["bk_file"]# taking new file path 
        filenaemEdit = secure_filename(bk_file.filename)#securing name of file 
        filepathEdit=os.path.join(app.config['UPLOAD_FOLDER'],filenaemEdit)#joining folder path with filename 
        bk_file.save(filepathEdit)#seving file to staric/img folder
        query = "UPDATE books SET bk_name = %s, bk_des = %s, bk_id=%s, file_path=%s WHERE dept = 'AIDS' AND sr_no = %s"
        values = (bk_name, bk_des, bk_id,filepathEdit,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        os.remove(old_filename)#removing old img from static/img folder
        cursor.close()
        return redirect("/edit_aids")
    else:
        return render_template("edit.html", book_data=book_data, dep="aids")

@app.route('/edit_csai')
def edit_csai():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'CSAI'")
    user = cur.fetchall()
    return render_template('edit_csai.html', user=user)

@app.route("/edit_in_bk_csai/<int:sr_no>", methods=["GET", "POST"])
def edit_in_csai(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books WHERE dept = 'CSAI' AND sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    old_filename = book_data['file_path']# retrieving old img path from db
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        bk_file = request.files["bk_file"]# taking new file path 
        filenaemEdit = secure_filename(bk_file.filename)#securing name of file 
        filepathEdit=os.path.join(app.config['UPLOAD_FOLDER'],filenaemEdit)#joining folder path with filename 
        bk_file.save(filepathEdit)#seving file to staric/img folder
        query = "UPDATE books SET bk_name = %s, bk_des = %s, bk_id=%s, file_path=%s WHERE dept = 'CSAI' AND sr_no = %s"
        values = (bk_name, bk_des, bk_id,filepathEdit,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        os.remove(old_filename)#removing old img from static/img folder
        cursor.close()
        return redirect("/edit_csai")
    else:
        return render_template("edit.html", book_data=book_data, dep="csai")

@app.route('/edit_csaiml')
def edit_csaiml():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM books where dept = 'CSAIML'")
    user = cur.fetchall()
    return render_template('edit_csaiml.html', user=user)

@app.route("/edit_in_bk_csaiml/<int:sr_no>", methods=["GET", "POST"])
def edit_in_csaiml(sr_no):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM books WHERE dept = 'CSAIML' AND sr_no = %s", (sr_no,))
    book_data = cursor.fetchone()
    old_filename = book_data['file_path']# retrieving old img path from db
    if request.method == "POST":
        bk_name = request.form["bk_name"]
        bk_des = request.form["bk_des"]
        bk_id = request.form["bk_id"]
        bk_file = request.files["bk_file"]# taking new file path 
        filenaemEdit = secure_filename(bk_file.filename)#securing name of file 
        filepathEdit=os.path.join(app.config['UPLOAD_FOLDER'],filenaemEdit)#joining folder path with filename 
        bk_file.save(filepathEdit)#seving file to staric/img folder
        query = "UPDATE books SET bk_name = %s, bk_des = %s, bk_id=%s, file_path=%s WHERE dept = 'CSAIML' AND sr_no = %s"
        values = (bk_name, bk_des, bk_id,filepathEdit,sr_no)
        cursor.execute(query, values)
        mysql.connection.commit()
        os.remove(old_filename)#removing old img from static/img folder
        cursor.close()
        return redirect("/edit_csaiml")
    else:
        return render_template("edit.html", book_data=book_data, dep="csaiml")
    
@app.route("/editBack")
def editBack():
    return redirect("/edit_book")

@app.route("/search" , methods=['GET'])
def search():
    query = request.args.get('search')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Execute the main query to fetch all columns for the search query
    sql_query = "SELECT * FROM books WHERE bk_name = %s"
    cursor.execute(sql_query, (query,))
    table_result = cursor.fetchall()
    
    # Execute a separate query to fetch the 'author' column for the same search query
    cursor.execute("SELECT author FROM books WHERE bk_name = %s", (query,))
    auth_result = cursor.fetchone()  # Use fetchone() to get a single result
    
    # Extract the 'author' value as a string
    auth = auth_result['author'] if auth_result else None
    
    # creating view for search
    cursor.execute("create or replace view search as select bk_name ,bk_id ,dept from books where author = %s", (auth,))

    cursor.execute("SELECT * FROM books WHERE author = %s", (auth,))
    author_books = cursor.fetchall()


    return render_template('search.html', result=table_result , author_books = author_books)



@app.route('/delete/<int:sr_no>' , methods=['GET' , 'POST'])
def delete(sr_no):
    previous_url = request.referrer

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    confirm = request.form.get('confirm')
    if confirm == "yes":
        #  table = request.form.get('table_name')
         cursor.execute("SELECT * FROM books WHERE sr_no = %s", (sr_no,))
         book_data = cursor.fetchone()
         try:
             file = book_data['file_path']
             cursor.execute('DELETE FROM books WHERE sr_no = %s', (sr_no,))
             mysql.connection.commit()
             os.remove(file)
         except Exception as e:
                 print("An error occurred:", str(e))
    
    cursor.close()
    return redirect(previous_url)



def process_form():
    global user_input  # Use the global keyword to modify the global variable
    user_input = request.form.get('user_input')
    # return f"You entered the number: {user_input}"


@app.route('/issue_book_chemical/<int:sr_no>', methods=['GET', 'POST'])

def issue_book_chemical(sr_no):
    previous_url = request.referrer
    if request.method == "POST":
        # current_datetime = datetime.datetime.now()

        current_datetime = datetime.datetime.now()
        currentdate = current_datetime.date()
        # print("I am here  1")

        
        
        
        details = request.form
        book1_name = details['book1_name']
        

        count = session.get('count', 0)
        count = 1
        session['count'] = count
        
        current_date_time = current_datetime.strftime("%B %d, %Y")

        # print("current date and time = ",current_date_time)
        date_time_return = currentdate   + timedelta(days=7) 
        

        datetime_return = date_time_return.strftime("%B %d, %Y")
        # date_time = details['current_datetime']
        # print("I am here  1")
        
        global scanning 
        scanning=True

        cap = cv2.VideoCapture(0)
        while scanning:
            ret, frame = cap.read() #This line reads a frame from the camera feed. ret is a boolean indicating whether the frame was successfully read, and frame contains the image data.
            if not ret:
                continue

            decoded_objects = decode(frame)
            for obj in decoded_objects:
                prn = obj.data.decode('utf-8')
                 
                # You can do something with the barcode data here.
                    
                    
                    # Stop scanning after a QR code is detected
                scanning = False

                cv2.imshow('Barcode Scanner', frame)
                if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit the barcode scanner.
                    break

        cap.release()
        cv2.destroyAllWindows()
        # print(f'Barcode Data: {barcode_data}')
        



        cur = mysql.connection.cursor()
        # details = request.form
        
        cur.execute("INSERT INTO book_issue (book1_name, date_time, prn, date_time_return, count) VALUES (%s, %s, %s, %s, %s)",
                   (book1_name, currentdate, prn, date_time_return, count))
        mysql.connection.commit()
        cur.close()
        # print("I am here  1")



        # current_datetime = datetime.datetime.now()
        # currentdate = current_datetime.date()
        
        # currentdate and date_time_return - > for equating 
        # current_date_time and datetime_return - > for format printing


        # current_dt_unfor = current_datetime;

       

        # print(date_time_return) 
        # print("The current date is ", currentdate)

        # print("the date of return of this book is ", date_time_return)

        
        # return render_template('Chemical.html',data=data)
            
        return render_template("layout.html", book1_name=book1_name, currentdate=currentdate,  date_time_return=date_time_return, current_date_time=current_date_time, datetime_return=datetime_return, count=count)
        
        
    # return render_template('add_book.html')




app.run(host="localhost", debug=True)
