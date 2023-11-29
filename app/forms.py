from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange

class RegisterLoginForm(FlaskForm):
    username = StringField(
        'Username: ',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password: ',
        validators=[DataRequired()]
    )