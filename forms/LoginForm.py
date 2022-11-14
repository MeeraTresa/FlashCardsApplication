from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField,EmailField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length, ValidationError, Email
class LoginForm(FlaskForm):
    email        = EmailField("Email",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=10, max=30, message="Email must be between 5 and 30 characters long")                                    
                                ])
    password     = PasswordField("Password",
                                validators=[
                                    InputRequired("Input is required!"),
                                    DataRequired("Data is required!"),
                                    Length(min=4, max=40, message="Password must be between 10 and 40 characters long")
                                ])
    submit       = SubmitField("Login")
