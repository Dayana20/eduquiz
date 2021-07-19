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
  
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # checks if entries are valid
        flash(f'{form.username.data} successfully logged in!', 'success')
        return redirect(url_for('home')) # if so - send to home page
    return render_template('register.html', title='Register', form=form)

  
  
  
if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")