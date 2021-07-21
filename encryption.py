# encryption.py
# 
# Has been created to declutter script.py
# Holds functions related to encryptions and initializes modules needed
#

from flask_bcrypt import Bcrypt #install flask-bcrypt


# Set up bcrypt for password hashing
bcrypt = Bcrypt()


# Give a password to encrpyt by salting and hashing
def encrypt_password(password):
    return bcrypt.generate_password_hash(password)
       

# Check if encrypted pasword and guess input password match, thus valid
def check_password_match(pw_hash, guess):
    return bcrypt.check_password_hash(pw_hash, guess) 
