from flask import Flask, render_template, url_for, flash, redirect
from registration_forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy

app = Flask(__name__)
proxied = FlaskBehindProxy(app)  
app.config['SECRET_KEY'] = 'e6d894ab9aa5e4b585f29ff83a43d75c'

@app.route("/")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/quizzes")
def quizzes():
    quizzes = ['Quiz 1', 'Quiz 2', 'Quiz 3']
    return render_template('quizzes.html', subtitle='Quiz Selection Page', altpass =quizzes)

@app.route('/my-link/')
def my_link():
    return render_template('home.html', subtitle='Home Page')

@app.route('/random/')
def random():
    quizzes = ['Random Quiz 1', 'Random Quiz 2', 'Random Quiz 3']
    return render_template('quizzes.html', subtitle='Quiz Selection Page', altpass =quizzes)

@app.route('/funny/')
def funny():
    quizzes = ['Funny Quiz 1', 'Funny Quiz 2', 'Funny Quiz 3']
    return render_template('quizzes.html', subtitle='Quiz Selection Page', altpass =quizzes)

@app.route('/educational/')
def educational():
    quizzes = ['educational Quiz 1', 'educational Quiz 2', 'educational Quiz 3']
    return render_template('quizzes.html', subtitle='Quiz Selection Page', altpass =quizzes)

@app.route('/countries/')
def countries():
    quizzes = ['countries Quiz 1', 'countries Quiz 2', 'countries Quiz 3']
    return render_template('quizzes.html', subtitle='Quiz Selection Page', altpass =quizzes)

@app.route('/languages/')
def languages():
    quizzes = ['languages Quiz 1', 'languages Quiz 2', 'languages Quiz 3']
    return render_template('quizzes.html', subtitle='Quiz Selection Page', altpass =quizzes)

@app.route('/technology/')
def technology():
    quizzes = ['technology Quiz 1', 'technology Quiz 2', 'technology Quiz 3']
    return render_template('quizzes.html', subtitle='Quiz Selection Page', altpass =quizzes)

@app.route('/food/')
def food():
    quizzes = ['food Quiz 1', 'food Quiz 2', 'food Quiz 3']
    return render_template('quizzes.html', subtitle='Quiz Selection Page', altpass =quizzes)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")