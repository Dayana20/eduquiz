from flask import Flask, render_template, url_for, flash, redirect, request
from registration_forms import RegistrationForm
from quiz_mainpage import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  
app.config['SECRET_KEY'] = 'e6d894ab9aa5e4b585f29ff83a43d75c'


@app.route("/")
def home():
    return render_template('home.html', subtitle='Home Page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route('/general_quiz/<string:quiz_data>', methods=['GET','POST'])
def general_quiz(quiz_data):
    #randomly select a quiz from sql table  
    data  = quiz_data.split(',')
    question = data[0][1:]
    options = data[1:]
    answer = " 'answer to question'])"
    if request.method== 'POST':
        user_answer = request.form.get('toReturn')
        print(user_answer, answer)
        if(user_answer==answer):
            flash('Correct!')
        else:
            flash('Incorrect! :(')
        return render_template('home.html', subtitle='Home Page')
    print("OPTIONS: ",options)
    return render_template('quiz.html', subtitle='Quiz',question=question,answer=answer,options=options )

# @app.route('/quiz_answer/', methods=['POST'])
# def post_quiz(quiz_answer):
#     if request.method== 'POST':
# #         answer = request.form('question') 
#         flash('Correct!')
#     return render_template('home.html', subtitle='Home Page')

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
    # zola = RegistrationForm()
    quizzes = {'Quiz 1':['option1','option2','option3','answer to question'], 'Quiz 2':['option1','option2','option3','answer to question']}
    return render_template('choose_quiz.html', altpass=quizzes)
    

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")