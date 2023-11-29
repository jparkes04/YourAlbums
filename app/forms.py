from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField
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

class AlbumForm(FlaskForm):
    title = StringField(
        'Album Title: ',
        validators=[DataRequired()]
    )
    artist = StringField(
        'Artist Name: ',
        validators=[DataRequired()]
    )
    year = IntegerField(
        'Year of Release: ',
        validators=[NumberRange(min=0)]
    )