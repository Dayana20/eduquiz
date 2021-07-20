from flask import Flask, render_template, url_for, flash, redirect
from registration_forms import RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import secrets


app = Flask(__name__)
proxied = FlaskBehindProxy(app)  
#print(secrets.token_hex(16))
app.config['SECRET_KEY'] = '0a85f9ea1879f713046952c8db9a1d6a'
db = SQLAlchemy(app)

# For storing user data
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.password}')"


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)
  

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'{form.username.data} successfully logged in!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('login.html', title='Login', form=form)


# Temp function so it can exist without error

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home Page', subtitle='Hub for the website')

@app.route("/quiz_page", methods=['GET', 'POST'])
def quiz_page():
    zola = RegistrationForm()
    return render_template('choose_quiz.html', title = 'Choose_quiz', form = zola)
    
if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")