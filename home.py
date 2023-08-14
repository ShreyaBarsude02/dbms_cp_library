from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/dbms_cp"
db = SQLAlchemy(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login')
def relogin():
    return render_template('login.html')

@app.route('/cards')
def cards():
    return render_template('cards.html')

@app.route('/buttons')
def buttons():
    return render_template('buttons.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/blank')
def blank():
    return render_template('blank.html')

@app.route('/404')
def _404error():
    return render_template('404.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/index')
def index():
    return render_template('index.html')

class create_acc(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(120), nullable=True)
    email_add = db.Column(db.String(120), unique=False, nullable=True)
    password = db.Column(db.String(120), nullable=True)
    repeat_password = db.Column(db.String(120), nullable=True)
    date_time = db.Column(db.String(120), nullable=True)
    phone_number = db.Column(db.String(120), nullable=True)
@app.route('/register',methods = ['POST', 'GET'])
def register():
    if (request.method=="POST"):
        """Add entries to the database"""
        fname=request.form.get("first_name")
        lname = request.form.get("last_name")
        email = request.form.get("email_add")
        passw = request.form.get("password")
        repeat_passw = request.form.get("repeat_password")
        phn= request.form.get("phn_no")

        if fname != '' and lname != '' and lname != '' and passw!='' and repeat_passw!='' and passw==repeat_passw:
            entry=create_acc(first_name=fname,last_name=lname,email_add=email,password=passw,repeat_passw=repeat_passw,date_time=datetime.now(),phone_number=phn)
            db.session.add(entry)
            db.session.commit()

            return render_template('index.html')

    return render_template('register.html')
app.run(debug=True)