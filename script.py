from flask import Flask, render_template, url_for, flash, redirect, request
from quiz_mainpage import RegistrationForm
from registration_forms import RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import secrets
from encryption import bcrypt, encrypt_password, check_password_match
from quiz import getting_dataframe, quizzes_display, get_options

from user_db import new_user, update_score, get_score
from plot_creation import *


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

###
# Helper Functions
###
 
# Give a password to encrpyt by salting and hashing
def encrypt_password(password):
    return bcrypt.generate_password_hash(password)
       

# Check if encrypted pasword and guess input password match, thus valid
def check_password_match(pw_hash, guess):
    return bcrypt.check_password_hash(pw_hash, guess) 
  
#register  

# Saves the value of the logged in user. 
# Uses the User class as inputs to log people in
class Login_Manager():
    def __init__(self):
        self.user = None #default not logged in
    
    # Login user by setting it to current user
    def login(self, user):
        self.user = user

    # Logout user by setting user to None
    def logout(self):
        self.user = None
    
    def is_logged_in(self):
        if self.user is None:
            return False
        return True
    
    def get_username(self):
        if not self.is_logged_in():
            return ""
        return self.user.username
    
    def get_email(self):
        if not self.is_logged_in():
            return ""
        return self.user.username
    
    def __str__(self):
        if self.is_logged_in():
            return f'Currently {self.user.username} is logged in'  
        else:
            return 'Nobody is currently logged in'

          
log_manage = Login_Manager()      



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

        # creating a user instance in user_data table
        new_user(user.id, user.username)

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
        log_manage.login(login_user)
        flash(f'{form.username.data} successfully logged in!', 'success')
        return redirect(url_for('user_page')) # if so - send to home page
        
    return render_template('login.html', title='Login', form=form)


# Temp function so it can exist without error
@app.route("/")
@app.route("/home")
def home():
    
    return render_template('home.html', title='',
                           subtitle='Hub for the website',
                           login_status=log_manage.is_logged_in())

class Question:
    def __init__(self):
        self.question = None
        self.answer = None
        self.options = None
    def get_answer():
        return self.answer
    def get_options():
        return self.options

df = getting_dataframe()
  
# defining question
question = Question()

@app.route('/general_quiz/<string:quiz_data>', methods=['GET','POST'])
def general_quiz(quiz_data):
    if not log_manage.is_logged_in():
        flash(f'You must login first!', 'danger')
        return redirect(url_for('login')) # if so - send to home page
    print(question.answer, question.options)
    if request.method == 'GET':
        question.answer, question.options = get_options(df, quiz_data)
        print(quiz_data,question.answer, question.options)
        if(isinstance(question.options,str)):
            question.options = question.options.split(',') 
    if request.method== 'POST':
        user_answer = request.form.get('toReturn')
        print([user_answer.strip(' ')],"++++",[question.answer.strip(' ')])
        if(user_answer.strip(' ')==question.answer.strip(' ')):
            flash('Correct!', 'success')
            if log_manage.is_logged_in():
                update_score(log_manage.get_username(), True)
        else:
            flash('Incorrect! :(', 'danger')
            if log_manage.is_logged_in():
                update_score(log_manage.get_username(), False)
        return redirect(url_for('user_page')) # if so - send to home page
    return render_template('quiz.html', subtitle='Quiz',question=quiz_data,answer=question.answer,options=question.options )

    
    
@app.route('/Animals/')
def Animals():
    df = getting_dataframe()
    data = quizzes_display(df, 'Animals')    
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Art/')
def Art():
    df = getting_dataframe()
    data = quizzes_display(df, 'Art')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Celebrities/')
def Celebrities():
    df = getting_dataframe()
    data = quizzes_display(df, 'Celebrities')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Board_Games/')
def Board_Games():
    df = getting_dataframe()
    data = quizzes_display(df, 'Entertainment: Board Games')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Books/')
def Books():
    df = getting_dataframe()
    data = quizzes_display(df, 'Entertainment: Books')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Cartoon_Animations/')
def Cartoon_Animations():
    df = getting_dataframe()
    data = quizzes_display(df, 'Entertainment: Cartoon & Animations')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Comics/')
def Comics():
    df = getting_dataframe()
    data = quizzes_display(df, 'Entertainment: Comics')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Film/')
def Film():
    df = getting_dataframe()
    data = quizzes_display(df, 'Entertainment: Film')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Anime_Manga/')
def Anime_Manga():
    df = getting_dataframe()
    data = quizzes_display(df, 'Entertainment: Japanese Anime & Manga')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Music/')
def Music():
    df = getting_dataframe()
    data = quizzes_display(df, 'Entertainment: Music')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Musicals_Theatres/')
def Musicals_Theatres():
    df = getting_dataframe()
    data = quizzes_display(df, 'Entertainment: Musicals & Theatres')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Television/')
def Television():
    df = getting_dataframe()
    data = quizzes_display(df, 'Entertainment: Television')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Video_Games/')
def Video_Games():
    df = getting_dataframe()
    data = quizzes_display(df, 'Entertainment: Video Games')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Geography/')
def Geography():
    df = getting_dataframe()
    data = quizzes_display(df, 'Geography')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/History/')
def History():
    df = getting_dataframe()
    data = quizzes_display(df, 'History')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Mythology/')
def Mythology():
    df = getting_dataframe()
    data = quizzes_display(df, 'Mythology')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Politics/')
def Politics():
    df = getting_dataframe()
    data = quizzes_display(df, 'Politics')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Science_Nature/')
def Science_Nature():
    df = getting_dataframe()
    data = quizzes_display(df, 'Science & Nature')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Science_Computers/')
def Science_Computers():
    df = getting_dataframe()
    data = quizzes_display(df, 'Science: Computers')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Science_Gadgets/')
def Science_Gadgets():
    df = getting_dataframe()
    data = quizzes_display(df, 'Science: Gadgets')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Science_Mathematics/')
def Science_Mathematics():
    df = getting_dataframe()
    data = quizzes_display(df, 'Science: Mathematics')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Sports/')
def Sports():
    df = getting_dataframe()
    data = quizzes_display(df, 'Sports')
    return render_template('choose_quiz.html', altpass =data)

@app.route('/Vehicles/')
def Vehicles():
    df = getting_dataframe()
    data = quizzes_display(df, 'Vehicles')
    return render_template('choose_quiz.html', altpass =data)


@app.route("/quiz_page", methods=['GET', 'POST'])
def quiz_page():
    df = getting_dataframe()
    data = quizzes_display(df, 'General Knowledge')
#     print(data) # answer,question,options
    if not log_manage.is_logged_in(): 
        flash(f'You must login first!', 'danger')
        return redirect(url_for('login')) # if so - send to home page
         
    # quizzes = {'Quiz 1':['option1','option2','option3','answer to question'], 'Quiz 2':['option1','option2','option3','answer to question']}
    return render_template('choose_quiz.html', altpass=data)


@app.route("/user_page/")
def user_page():
    if not log_manage.is_logged_in():
        flash(f'You must login first!', 'danger')
        return redirect(url_for('login')) # if so - send to home page
        
    username = log_manage.get_username()    
    score = get_score(username)
    anthony_score = get_score("anthony")
    berniel_score = get_score("berniel")
    dayana_score = get_score("dayana")
    fitsum_score = get_score("fitsum")
    # NOTE FOR DEV, REMOVE FOR FINAL PRODUCT
    # Create htmlstring based on data
    #
    # 1) Get data for specific username
    # 2) Set up arrays for data axis to pass
    # 3) Call functions:
    # Example:   
    xArray = [username, "anthony", "fitsum", "dayana", "berniel"]
    yArray = [score,anthony_score,fitsum_score,dayana_score,berniel_score]
    htmlString = create_bar_html(xArray,
                                "Usernames",
                                 yArray,
                                 "Total Points Earned",
                                 "Your score compared to our team\'s!")

    return render_template('user_page.html', title=f'Welcome, {username}!',
                           subtitle=f'This is your performance compared to our team\'s!',
                           plot=htmlString)

  

@app.route("/logout")
def logout():
    # Logout current user logged in
    
    flash(f'{log_manage.get_username()} logged out successfully', 'success')
    
    log_manage.logout()
    return redirect(url_for('login')) # if so - send to home page



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")