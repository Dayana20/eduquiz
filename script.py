from flask import Flask, render_template, url_for, flash, redirect, request
from quiz_mainpage import RegistrationForm
from registration_forms import RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import secrets
from encryption import bcrypt, encrypt_password, check_password_match
from user_db import create_dataframe, db_to_dataframe, new_user
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


# Saves the value of the logged in user. 
# Uses the User class as inputs to log people in
class Login_Manager():
    def __init__(self):
        self.user = None #default not logged in
    
    # Login user by setting it to current user
    def login(self, user):
        self.user = user

    # Logout user by setting user to None
    def logout(self, user):
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
        return redirect(url_for('home')) # if so - send to home page
        
    return render_template('login.html', title='Login', form=form)


# Temp function so it can exist without error
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home Page',
                           subtitle='Hub for the website')

@app.route('/general_quiz/<string:quiz_data>', methods=['GET','POST'])
def general_quiz(quiz_data):
    if not log_manage.is_logged_in():
        flash(f'You must login first!', 'danger')
        return redirect(url_for('login')) # if so - send to home page


    #randomly select a quiz from sql table  
    data  = quiz_data.split(',')
    question = data[0][1:]
    options = data[1:]
    answer = " 'answer to question'])"
    if request.method== 'POST':
        user_answer = request.form.get('toReturn')
        if(user_answer==answer):
            flash('Correct!')
        else:
            flash('Incorrect! :(')
        return render_template('home.html', subtitle='Home Page')
    return render_template('quiz.html', subtitle='Quiz',question=question,answer=answer,options=options )


@app.route('/random/')
def random():
    quizzes = {'Random Quiz 1':['option1','option2','option3','answer to question'], 'Random Quiz 2':['option1','option2','option3','answer to question']}
    
    return render_template('choose_quiz.html', altpass =quizzes)

@app.route('/funny/')
def funny():
    quizzes = {'funny Quiz 1':['option1','option2','option3','answer to question'], 'funny Quiz 2':['option1','option2','option3','answer to question']}
    return render_template('choose_quiz.html', altpass =quizzes)

@app.route('/educational/')
def educational():
    quizzes = {'educational Quiz 1':['option1','option2','option3','answer to question'], 'educational Quiz 2':['option1','option2','option3','answer to question']}

    return render_template('choose_quiz.html', altpass =quizzes)

@app.route('/countries/')
def countries():
    quizzes = {'countries Quiz 1':['option1','option2','option3','answer to question'], 'countries Quiz 2':['option1','option2','option3','answer to question']}

    return render_template('choose_quiz.html', altpass =quizzes)

@app.route('/languages/')
def languages():
    quizzes = {'languages Quiz 1':['option1','option2','option3','answer to question'], 'languages Quiz 2':['option1','option2','option3','answer to question']}

    return render_template('choose_quiz.html', altpass =quizzes)

@app.route('/technology/')
def technology():
    quizzes = {'technology Quiz 1':['option1','option2','option3','answer to question'], 'technology Quiz 2':['option1','option2','option3','answer to question']}

    return render_template('choose_quiz.html', altpass =quizzes)

@app.route('/food/')
def food():
    quizzes = {'food Quiz 1':['option1','option2','option3','answer to question'], 'food Quiz 2':['option1','option2','option3','answer to question']}

    return render_template('choose_quiz.html', altpass =quizzes)


@app.route("/quiz_page", methods=['GET', 'POST'])
def quiz_page():
    if not log_manage.is_logged_in():
        flash(f'You must login first!', 'danger')
        return redirect(url_for('login')) # if so - send to home page
         
    quizzes = {'Quiz 1':['option1','option2','option3','answer to question'], 'Quiz 2':['option1','option2','option3','answer to question']}
    return render_template('choose_quiz.html', altpass=quizzes)


@app.route("/user_page/")
def user_page():
    if not log_manage.is_logged_in():
        flash(f'You must login first!', 'danger')
        return redirect(url_for('login')) # if so - send to home page
        
  
    username = log_manage.get_username()    
    
    # Create htmlstring based on data
    #
    # 1) Get data for specific username
    # 2) Set up arrays for data axis to pass
    # 3) Call functions:
    #   
    #   htmlString = create_bar_html(x-axisArray,
    #                                x-label,
    #                                y-axisArray,
    #                                y-label,
    #                                "plotTitle")
    
    # DEBUG SAMPLE: for proof of concept
    htmlString = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoAAAAHgCAYAAAA10dzkAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjMuNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8QVMy6AAAACXBIWXMAAA9hAAAPYQGoP6dpAABRVElEQVR4nO3dd3hUZf7+8XsSSAKEBKkJLfQSwUIRgihFEBSRZgFRisoqS5G2IiIgNlD2J+qquJYFFLCgFAEBlbpAkI6yKAIiQUyClCQUEyB5fn/km5EhCaTNzJk579d15brMmZMznzPF+fA857nHYYwxAgAAgG0EeLsAAAAAeBYNIAAAgM3QAAIAANgMDSAAAIDN0AACAADYDA0gAACAzdAAAgAA2AwNIAAAgM3QAAIAANgMDSAAAIDN0AACAADYDA0gAACAzdAAAgAA2AwNIAAAgM3QAAIAANgMDSAAAIDN0AACAADYDA0gAACAzdAAAgAA2AwNIAAAgM3QAAIAANgMDSAAAIDN0AACAADYDA0gAACAzdAAAgAA2AwNIAAAgM3QAAIAANgMDSAAAIDN0AACAADYDA0gAACAzdAAAgAA2AwNIAAAgM3QAAIAANgMDSAAAIDN0AACKJQaNWpowIABRXrMtWvXyuFwaO3atUV6XH8yYMAA1ahRw9tlWE7Wa+fzzz+/4n6zZs2Sw+HQr7/+6pnCAIuhAYQt/PDDD7rnnnsUFRWlkJAQValSRR07dtS//vUvb5d2Rc8++6wcDofzp2TJkoqOjtYzzzyjlJQUb5fnUfPmzdNrr71W5Me99PF1OBwqVaqUoqOj9cILL+jcuXNFfn/eYIzRRx99pFtvvVVlypRRyZIl1bhxYz333HM6e/Zskd/f5Y9pWFiY2rRpo2XLlhX5fQEomGLeLgBwt02bNqldu3aqXr26Bg0apIiICB05ckSbN2/W66+/rmHDhnm7xKuaMWOGQkNDdebMGX399dd68cUXtXr1am3cuFEOh8Pb5RW5W2+9VX/++aeCgoKc2+bNm6c9e/ZoxIgRRX5/HTt2VL9+/SRJZ86c0X//+19NmDBBu3fv1vz584v8/jwpPT1dDzzwgD777DPdcsstevbZZ1WyZEn997//1eTJkzV//nx9++23qlSpUpHeb9ZjaozR4cOHNWPGDHXt2lXLly9Xp06divS+CuKhhx5S7969FRwc7O1SAK+gAYTfe/HFFxUeHq6tW7eqTJkyLrcdO3bMO0Xl0z333KPy5ctLkh5//HH16tVLCxYs0ObNmxUTE+Pl6opOamqqgoKCFBAQoJCQEI/db7169fTggw86f3/88cd1/vx5LViwQKmpqR6tpai98sor+uyzzzRmzBhNmzbNuf1vf/ub7rvvPnXv3l0DBgzQ8uXLi/R+L39Me/XqpejoaL3++uuWaAADAwMVGBjo7TIAr2EKGH7v4MGDuvbaa7M1f5JUsWJFl98vXryo559/XrVr11ZwcLBq1Kihp59+WmlpaS771ahRQ3fddZc2bNigm266SSEhIapVq5Y+/PDDbPfx/fffq02bNipRooSqVq2qF154QTNnzizU9Uft27eXJB06dEiSdPbsWY0ePVrVqlVTcHCw6tevr3/+858yxrj8ncPh0NChQzV37lzVr19fISEhatq0qdavX++yX27Xl2VNSV/JyZMnNWbMGDVu3FihoaEKCwvTHXfcod27d7vsl3Wt1ieffKJnnnlGVapUUcmSJZWSkpLtGsC2bdtq2bJlOnz4sHNasUaNGjpz5oxKlSqlJ554Ilsdv/32mwIDAzVlypQr1pubiIgIORwOFSv217+T//vf/+ree+9V9erVFRwcrGrVqmnkyJH6888/Xf42ISFBAwcOVNWqVRUcHKzIyEh169Yt2/O9fPly3XLLLSpVqpRKly6tLl266H//+1+2WhYtWqRGjRopJCREjRo10sKFC/N0Dn/++aemTZumevXq5fg4dO3aVf3799eKFSu0efNm5/b8vL7zqmHDhipfvrwOHjzosn3x4sXq0qWLKleurODgYNWuXVvPP/+80tPTXfZr27atGjVqpL1796pdu3YqWbKkqlSpoldeeeWq952Wlqa77rpL4eHh2rRpk6ScrwH09vsa8CRGAOH3oqKiFBsbqz179qhRo0ZX3PfRRx/V7Nmzdc8992j06NH67rvvNGXKFP3444/ZPnQPHDige+65R4888oj69++v//znPxowYICaNm2qa6+9VpJ09OhRtWvXTg6HQ+PGjVOpUqX0/vvvF3raKetDtFy5cjLG6O6779aaNWv0yCOP6IYbbtDKlSv1j3/8Q0ePHtX06dNd/nbdunX69NNPNXz4cAUHB+vtt99W586dtWXLlqs+Pnnxyy+/aNGiRbr33ntVs2ZN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KIB72DFaCbBMDIyU+ZVwAwcOVKVKlbRz507ddNNNKleunH755Rfdcccd3i4P8DqiUICiZedoJdibpWJgGjRooEmTJqlPnz4qXbq0du/erVq1amnixIk6efKk3nzzTW+X6IJl5PAWpquAwiNayb74/LbYCGBcXJxatWolSSpRooROnz4tSXrooYf08ccfe7M0wFKyolC63VBFMbXL8eEEFEB+opUAf2OpBjAiIkInT2a+0apXr67NmzdLyvyuYAsNVAIA/ADRSrAzSzWA7du315dffilJGjhwoEaOHKmOHTvq/vvvV48ePbxcHQDAnxCtlCk9wyj24Akt3nVUsQdPKD2DARc7sNQq4HfffVcZGRmSpCFDhqhcuXLatGmT7r77bj322GNerg4A4E+IVmIFtJ1ZahGIr+EiUgDwbVmrgKWco5X8eXV91rlf3gTY4dz5/LbYCKAkJSUlacuWLTp27JhzNDBLv379vFQVAMAfZUUrXT4KFuHno2DpGUaTl+zNceTTKLMJnLxkrzpGR7DIzE9ZqgFcsmSJ+vbtqzNnzigsLEwOx18vOofDQQMIAChynRtFqmN0hK2ilfKzAjqmdjnPFQaPsVQDOHr0aD388MN66aWXVLJkSW+XAwCwiaxoJbtgBTQstQr46NGjGj58OM0fAABuxApoWKoB7NSpk7Zt2+btMgAA8GtZK6Bzm+R2KHM1cE4roImN8Q9enwLOyv2TpC5duugf//iH9u7dq8aNG6t48eIu+959992eLg8AAL8TGODQpK7RGjxnhxzKeQX0pK7R2a6DJDbGf3g9BiYgIG+DkA6HQ+np6W6uJn9YRg4A8GX5aej8KTaGz28LjABeHvUCAAA8I68roImN8T9ebwABAID35GUFNLEx/scSi0BWr16t6OhopaSkZLstOTlZ1157rdavX++FygAAALEx/scSDeBrr72mQYMG5TgPHx4erscee0zTp0/3QmUAAIDYGP9jiQZw9+7d6ty5c66333777dq+fbsHKwIA4MrsFIdSmNgYWJMlGsDExMRskS+XKlasmP744498HXPKlClq3ry5SpcurYoVK6p79+7at2+fyz6pqakaMmSIypUrp9DQUPXq1UuJiYkFOgcAgH2s2BOv1i+vVp/3NuuJT3apz3ub1frl1VqxJ97bpblFVmyMpGxN4JViY2BdlmgAq1Spoj17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ts4BLCxyhAAA8D18ftv4GkAAAAC7ogEEAACwGVtfA1hYWbPnfCMIAAC+I+tz285XwdEAFsLp06cliW8EAQDAB50+fVrh4eHeLsMrWARSCBkZGfr9999VunRpORy+92XbKSkpqlatmo4cOWKri2Dtet6Sfc/dructce52PHe7nreU93M3xuj06dOqXLmyAgLseTUcI4CFEBAQoKpVq3q7jEILCwuz3f8kJPuet2Tfc7freUucux3P3a7nLeXt3O068pfFnm0vAACAjdEAAgAA2AwNoI0FBwdr0qRJCg4O9nYpHmXX85bse+52PW+Jc7fjudv1vCV7n3t+sQgEAADAZhgBBAAAsBkaQAAAAJuhAQQAALAZGkAAAACboQG0gaNHj+rBBx9UuXLlVKJECTVu3Fjbtm1z3j5gwAA5HA6Xn86dO3ux4qJRo0aNbOflcDg0ZMgQSVJqaqqGDBmicuXKKTQ0VL169VJiYqKXqy68q51327Zts932+OOPe7nqopGenq4JEyaoZs2aKlGihGrXrq3nn3/e5fs+jTGaOHGiIiMjVaJECXXo0EH79+/3YtWFl5fz9tf3uZT5dV4jRoxQVFSUSpQooVatWmnr1q3O2/3xOZeuft7+8pyvX79eXbt2VeXKleVwOLRo0SKX2/Py/J48eVJ9+/ZVWFiYypQpo0ceeURnzpzx4FlYkIFfO3nypImKijIDBgww3333nfnll1/MypUrzYEDB5z79O/f33Tu3NnEx8c7f06ePOnFqovGsWPHXM7pm2++MZLMmjVrjDHGPP7446ZatWpm1apVZtu2baZly5amVatW3i26CFztvNu0aWMGDRrksk9ycrJ3iy4iL774oilXrpxZunSpOXTokJk/f74JDQ01r7/+unOfqVOnmvDwcLNo0SKze/duc/fdd5uaNWuaP//804uVF05ezttf3+fGGHPfffeZ6Ohos27dOrN//34zadIkExYWZn777TdjjH8+58Zc/bz95Tn/6quvzPjx482CBQuMJLNw4UKX2/Py/Hbu3Nlcf/31ZvPmzea///2vqVOnjunTp4+Hz8RaaAD93NixY03r1q2vuE///v1Nt27dPFOQFz3xxBOmdu3aJiMjwyQlJZnixYub+fPnO2//8ccfjSQTGxvrxSqL3qXnbUxmA/jEE094tyg36dKli3n44YddtvXs2dP07dvXGGNMRkaGiYiIMNOmTXPenpSUZIKDg83HH3/s0VqL0tXO2xj/fZ+fO3fOBAYGmqVLl7psb9KkiRk/frzfPudXO29j/PM5v7wBzMvzu3fvXiPJbN261bnP8uXLjcPhMEePHvVY7VbDFLCf+/LLL9WsWTPde++9qlixom688Ua999572fZbu3atKlasqPr162vw4ME6ceKEF6p1n/Pnz2vOnDl6+OGH5XA4tH37dl24cEEdOnRw7tOgQQNVr15dsbGxXqy0aF1+3lnmzp2r8uXLq1GjRho3bpzOnTvnxSqLTqtWrbRq1Sr9/PPPkqTdu3drw4YNuuOOOyRJhw4dUkJCgsvzHh4erhYtWvj08361887ij+/zixcvKj09XSEhIS7bS5QooQ0bNvjtc361887ij8/5pfLy/MbGxqpMmTJq1qyZc58OHTooICBA3333ncdrtopi3i4A7vXLL79oxowZGjVqlJ5++mlt3bpVw4cPV1BQkPr37y9J6ty5s3r27KmaNWvq4MGDevrpp3XHHXcoNjZWgYGBXj6DorFo0SIlJSVpwIABkqSEhAQFBQWpTJkyLvtVqlRJCQkJni/QTS4/b0l64IEHFBUVpcqVK+v777/X2LFjtW/fPi1YsMB7hRaRp556SikpKWrQoIECAwOVnp6uF198UX379pUk53NbqVIll7/z9ef9auct+e/7vHTp0oqJidHzzz+vhg0bqlKlSvr4448VGxurOnXq+O1zfrXzlvz3Ob9UXp7fhIQEVaxY0eX2YsWKqWzZsj79GigsGkA/l5GRoWbNmumll16SJN14443as2eP3nnnHWcD2Lt3b+f+jRs31nXXXafatWtr7dq1uu2227xSd1H74IMPdMcdd6hy5creLsWjcjrvv/3tb87/bty4sSIjI3Xbbbfp4MGDql27tjfKLDKfffaZ5s6dq3nz5unaa6/Vrl27NGLECFWuXNn5evdHeTlvf36ff/TRR3r44YdVpUoVBQYGqkmTJurTp4+2b9/u7dLc6mrn7c/POQqPKWA/FxkZqejoaJdtDRs2VFxcXK5/U6tWLZUvX14HDhxwd3kecfjwYX377bd69NFHndsiIiJ0/vx5JSUlueybmJioiIgID1foHjmdd05atGghSX7xfP/jH//QU089pd69e6tx48Z66KGHNHLkSE2ZMkWSnM/t5au9ff15v9p558Sf3ue1a9fWunXrdObMGR05ckRbtmzRhQsXVKtWLb99zqUrn3dO/Ok5z5KX5zciIkLHjh1zuf3ixYs6efKkz78GCoMG0M/dfPPN2rdvn8u2n3/+WVFRUbn+zW+//aYTJ04oMjLS3eV5xMyZM1WxYkV16dLFua1p06YqXry4Vq1a5dy2b98+xcXFKSYmxhtlFrmczjsnu3btkiS/eL7PnTungADX/60FBgYqIyNDklSzZk1FRES4PO8pKSn67rvvfPp5v9p558Tf3ueSVKpUKUVGRurUqVNauXKlunXr5rfP+aVyOu+c+ONznpfnNyYmRklJSS4jwqtXr1ZGRobzH8C25O1VKHCvLVu2mGLFipkXX3zR7N+/38ydO9eULFnSzJkzxxhjzOnTp82YMWNMbGysOXTokPn2229NkyZNTN26dU1qaqqXqy+89PR0U716dTN27Nhstz3++OOmevXqZvXq1Wbbtm0mJibGxMTEeKHKopfbeR84cMA899xzZtu2bebQoUNm8eLFplatWubWW2/1UqVFq3///qZKlSrOOJQFCxaY8uXLmyeffNK5z9SpU02ZMmXM4sWLzffff2+6devm85EgVztvf3+fr1ixwixfvtz88ssv5uuvvzbXX3+9adGihTl//rwxxj+fc2OufN7+9JyfPn3a7Ny50+zcudNIMq+++qrZuXOnOXz4sDEmb89v586dzY033mi+++47s2HDBlO3bl1iYLxdANxvyZIlplGjRiY4ONg0aNDAvPvuu87bzp07Z26//XZToUIFU7x4cRMVFWUGDRpkEhISvFhx0Vm5cqWRZPbt25fttj///NP8/e9/N9dcc40pWbKk6dGjh4mPj/dClUUvt/OOi4szt956qylbtqwJDg42derUMf/4xz/8JgcwJSXFPPHEE6Z69eomJCTE1KpVy4wfP96kpaU598nIyDATJkwwlSpVMsHBwea2227L8fXhS6523v7+Pv/0009NrVq1TFBQkImIiDBDhgwxSUlJztv98Tk35srn7U/P+Zo1a4ykbD/9+/c3xuTt+T1x4oTp06ePCQ0NNWFhYWbgwIHm9OnTXjgb63AYc0lUPAAAAPwe1wACAADYDA0gAACAzdAAAgAA2AwNIAAAgM3QAAIAANgMDSAAAIDN0AACAADYDA0gAL/Rtm1bjRgxotDHefbZZ3XDDTcU+jjeVFSPBQD/RAMIoNAGDBggh8Mhh8OhoKAg1alTR88995wuXrzo7dIKZMyYMS7fLTpgwAB179690MedNWuW83EKCAhQZGSk7r//fsXFxRX62ACQHzSAAIpE586dFR8fr/3792v06NF69tlnNW3aNG+XlS/GGF28eFGhoaEqV66cW+4jLCxM8fHxOnr0qL744gvt27dP9957r1vuCwByQwMIoEgEBwcrIiJCUVFRGjx4sDp06KAvv/xSknTq1Cn169dP11xzjUqWLKk77rhD+/fvd/7trFmzVKZMGS1atEh169ZVSEiIOnXqpCNHjjj3yWkUbsSIEWrbtm2uNX300Udq1qyZSpcurYiICD3wwAM6duyY8/a1a9fK4XBo+fLlatq0qYKDg7VhwwaXKeBnn31Ws2fP1uLFi52jd2vXrlX79u01dOhQl/v7448/FBQU5DJ6eDmHw6GIiAhFRkaqVatWeuSRR7RlyxalpKQ49xk7dqzq1aunkiVLqlatWpowYYIuXLjgvD2rvo8++kg1atRQeHi4evfurdOnT+d6v8uWLVN4eLjmzp2b6z4A7IMGEIBblChRQufPn5eU2bxt27ZNX375pWJjY2WM0Z133unS1Jw7d04vvviiPvzwQ23cuFFJSUnq3bt3oWq4cOGCnn/+ee3evVuLFi3Sr7/+qgEDBmTb76mnntLUqVP1448/6rrrrnO5bcyYMbrvvvucI5zx8fFq1aqVHn30Uc2bN09paWnOfefMmaMqVaqoffv2earv2LFjWrhwoQIDAxUYGOjcXrp0ac2aNUt79+7V66+/rvfee0/Tp093+duDBw9q0aJFWrp0qZYuXap169Zp6tSpOd7PvHnz1KdPH82dO1d9+/bNU20A/FsxbxcAwL8YY7Rq1SqtXLlSw4YN0/79+/Xll19q48aNatWqlSRp7ty5qlatmhYtWuSc/rxw4YLefPNNtWjRQpI0e/ZsNWzYUFu2bNFNN91UoFoefvhh53/XqlVLb7zxhpo3b64zZ84oNDTUedtzzz2njh075niM0NBQlShRQmlpaYqIiHBu79mzp4YOHarFixfrvvvuk5Q5kpl1PWRukpOTFRoaKmOMzp07J0kaPny4SpUq5dznmWeecf53jRo1NGbMGH3yySd68sknndszMjI0a9YslS5dWpL00EMPadWqVXrxxRdd7u+tt97S+PHjtWTJErVp0yb3BwuArdAAAigSS5cuVWhoqC5cuKCMjAw98MADevbZZ7Vq1SoVK1bM2dhJUrly5VS/fn39+OOPzm3FihVT8+bNnb83aNBAZcqU0Y8//ljgBnD79u169tlntXv3bp06dUoZGRmSpLi4OEVHRzv3a9asWb6PHRISooceekj/+c9/dN9992nHjh3as2ePc9o7N6VLl9aOHTt04cIFLV++XHPnzs3WtH366ad64403dPDgQZ05c0YXL15UWFiYyz41atRwNn+SFBkZ6TK9LUmff/65jh07po0bN7o8tgDAFDCAItGuXTvt2rVL+/fv159//qnZs2e7jGoVVkBAgIwxLtsunUK+3NmzZ9WpUyeFhYVp7ty52rp1qxYuXChJzqnpLAWt89FHH9U333yj3377TTNnzlT79u0VFRV11fOoU6eOGjZsqFGjRqlly5YaPHiw8/bY2Fj17dtXd955p5YuXaqdO3dq/Pjx2WouXry4y+8Oh8PZ4Ga58cYbVaFCBf3nP//J9tgBsDcaQABFolSpUqpTp46qV6+uYsX+mlxo2LChLl68qO+++8657cSJE9q3b5/LKNzFixe1bds25+/79u1TUlKSGjZsKEmqUKGC4uPjXe5z165dudbz008/6cSJE5o6dapuueUWNWjQINsIWV4FBQUpPT092/bGjRurWbNmeu+99zRv3jyXKee8euqpp/Tpp59qx44dkqRNmzYpKipK48ePV7NmzVS3bl0dPny4QHXXrl1ba9as0eLFizVs2LACHQOAf6IBBOBWdevWVbdu3TRo0CBt2LBBu3fv1oMPPqgqVaqoW7duzv2KFy+uYcOG6bvvvtP27ds1YMAAtWzZ0jn92759e23btk0ffvih9u/fr0mTJmnPnj253m/16tUVFBSkf/3rX/rll1/05Zdf6vnnny/QOdSoUUPff/+99u3bp+PHj7uMPD766KOaOnWqjDHq0aNHvo9drVo19ejRQxMnTpSU+XjFxcXpk08+0cGDB/XGG284Ry4Lol69elqzZo2++OILgqEBONEAAnC7mTNnqmnTprrrrrsUExMjY4y++uorl2nMkiVLauzYsXrggQd08803KzQ0VJ9++qnz9k6dOmnChAl68skn1bx5c50+fVr9+vXL9T4rVKigWbNmaf78+YqOjtbUqVP1z3/+s0D1Dxo0SPXr11ezZs1UoUIFbdy40Xlbnz59VKxYMfXp00chISEFOv7IkSO1bNkybdmyRXfffbdGjhypoUOH6oYbbtCmTZs0YcKEAh03S/369bV69Wp9/PHHGj16dKGOBcA/OAwXhgDwslmzZmnEiBFKSkrydin59uuvv6p27draunWrmjRp4u1yACBPWAUMAAVw4cIFnThxQs8884xatmxJ8wfApzAFDAAFsHHjRkVGRmrr1q165513vF0OAOQLU8AAAAA2wwggAACAzdAAAgAA2AwNIAAAgM3QAAIAANgMDSAAAIDN0AACAADYDA0gAACAzdAAAgAA2AwNIAAAgM38f7jIR4Q4r8f3AAAAAElFTkSuQmCC"
    
    return render_template('user_page.html', title=f'Welcome {username}',
                           subtitle=f'This is the webpage for {username}',
                           plot=htmlString)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")