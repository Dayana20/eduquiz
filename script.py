from flask import Flask, render_template, url_for, flash, redirect
from registration_forms import RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import secrets
from encryption import bcrypt, encrypt_password, check_password_match

app = Flask(__name__)
proxied = FlaskBehindProxy(app)  
#print(secrets.token_hex(16))
app.config['SECRET_KEY'] = '0a85f9ea1879f713046952c8db9a1d6a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# For storing user data
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.password}')" 
  
# Saves the value of the logged in user. 
# Uses the User class as inputs to log people in
class Login_Manager():
    def __init__(self):
        self.user = None
    
    # Login user by setting it to current user
    def login(user):
        self.user = user

    # Logout user by setting user to None
    def logout(user):
        self.user = None
    
    
    def __str__(self):
        if self.user is None:
            return 'Nobody is currently logged in'
        else:
            return f'Currently {sel.user.username} is logged in'

          
          
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        
        # Check database if username is already in use
        exist_user = User.query.filter_by(username=form.username.data).first()
        if exist_user is not None:
            flash(f'Username {exist_user.username} is already taken', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        # Check database if email is already in use
        exist_user = User.query.filter_by(email=form.email.data).first()
        if exist_user is not None:
            flash(f'Email {exist_user.email} is already taken', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        # User can be registered
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password= encrypt_password(form.password.data))
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)
  

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # checks if entries are valid
        login_user = User.query.filter_by(username=form.username.data).first()
        
        # Username does not exist
        if login_user is None:
            flash(f'Username {form.username.data} does not exist!', 'danger')
            return render_template('login.html', title='Login', form=form)
        
        #Incorrect Password
        if not check_password_match(login_user.password, form.password.data):
            flash(f'Incorrect password ', 'danger')
            return render_template('login.html', title='Login', form=form)
        
        # Successful Login
        flash(f'{form.username.data} successfully logged in!', 'success')
        return redirect(url_for('home')) # if so - send to home page
        
    return render_template('login.html', title='Login', form=form)


# Temp function so it can exist without error
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home Page',
                           subtitle='Hub for the website')

@app.route("/quiz_page", methods=['GET', 'POST'])
def quiz_page():
    zola = RegistrationForm()
    return render_template('choose_quiz.html', title = 'Choose_quiz', form = zola)
    

@app.route("/user_page/")
def user_page():
    username = "hello"
    return render_template('user_page.html', title=f'Welcome {username}',
                           subtitle=f'This is the webpage for {username}')

    
if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")