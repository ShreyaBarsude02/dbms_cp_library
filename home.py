from flask import Flask,render_template
app = Flask(__name__)

@app.route('/')
def login():
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

app.run(debug=True)