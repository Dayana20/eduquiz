from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# Validator that checks for alphanumeric inputs (only letters or numbers)
def validate_alphanumeric(form, field):
    for i in field.data:
        ascii_i = ord(i)
        is_number = (48 <= ascii_i) and (ascii_i <= 57)
        is_letter_cap = (65 <= ascii_i) and (ascii_i <= 90)
        is_letter_low = (97 <= ascii_i) and (ascii_i <= 122)
        
        if not (is_number or is_letter_cap or is_letter_low):
            raise ValidationError('Field must be alphanumeric')


# Form for registering to an account
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20),
                                                   validate_alphanumeric])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up') 

# Form to login to an account
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), 
                                                   Length(min=2, max=20),
                                                   validate_alphanumeric])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login Up') 
