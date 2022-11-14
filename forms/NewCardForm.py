from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField,EmailField
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length, ValidationError, Email


class NewCardForm(FlaskForm):
    question = StringField("Question")
    answer = TextAreaField("Answer")
    submit = SubmitField("Create")