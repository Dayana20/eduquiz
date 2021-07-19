from flask import Flask, render_template, url_for, flash, redirect
from registration_forms import RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
proxied = FlaskBehindProxy(app)  
app.config['SECRET_KEY'] = 'e6d894ab9aa5e4b585f29ff83a43d75c'
db = SQLAlchemy(app)

# For storing user data
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.password}')"



@app.route("/")
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
@app.route("/home")
def home():
    return render_template('home.html', title='Home Page', subtitle='Hub for the website')

  
  
if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")