from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_user, LoginManager, UserMixin, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/dbms_cp"
db = SQLAlchemy(app)

# LoginManager is needed for our application
# to be able to log in and out users
login_manager = LoginManager()
login_manager.init_app(app)

class create_acc(UserMixin,db.Model):
    sr_no = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(120), nullable=True)
    email_add = db.Column(db.String(120), unique=False, nullable=True)
    password = db.Column(db.String(120), nullable=True)
    repeat_password = db.Column(db.String(120), nullable=True)
    date_time=db.Column(db.String(120), nullable=True)
    phone_number = db.Column(db.String(120), nullable=True)

    def get_id(self):
        return str(self.sr_no)

with app.app_context():
    db.create_all()

# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return create_acc.query.get(user_id)

@app.route("/")
def login1():
    return render_template('login.html')

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = create_acc.query.filter_by(email_add=request.form.get("email_add")).first()
        # Check if the password entered is the
        # same as the user's password
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            return redirect(url_for("index"))
        # Redirect the user back to the home
        else:
            flash('Invalid email or password.')
            return render_template("login.html")
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


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


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register',methods = ['POST', 'GET'])
def register():
    if (request.method=="POST"):
        """Add entries to the database"""
        first_name=request.form.get("first_name")
        last_name = request.form.get("last_name")
        email_add = request.form.get("email_add")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")
        phone_number= request.form.get("phone_number")

        user = create_acc.query.filter_by(email_add=email_add).first()  # if this returns a user, then the email already exists in database

        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return render_template("register.html")

        else:
            if password == repeat_password:
                entry=create_acc(first_name=first_name, last_name=last_name, email_add=email_add, password=password, repeat_password=repeat_password, date_time=datetime.now(),phone_number=phone_number)
                db.session.add(entry)
                db.session.commit()

                # Log the user in
                login_user(entry)

                # Redirect to the authenticated page
                return redirect(url_for('index'))

    return render_template('register.html')
app.run(debug=True)