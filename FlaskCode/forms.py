import sys 
sys.dont_write_bytecode = True
#Need to do the following installs:
# pip install flask-wtf
# pip install email_validator
from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, validators, ValidationError

class ContactForm(Form):
    name = StringField("Name",  [validators.InputRequired("Please enter your name.")])
    email = StringField("Email",  [validators.InputRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
    subject = StringField("Subject",  [validators.InputRequired("Please enter a subject.")])
    message = TextAreaField("Message",  [validators.InputRequired("Please enter a message.")])
    submit = SubmitField("Send") 