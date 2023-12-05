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
        validators=[DataRequired(), NumberRange(min=0)]
    )

class TrackForm(FlaskForm):
    position = IntegerField(
        'Position: ',
        validators=[DataRequired(), NumberRange(min=0)]
    )
    trackname = StringField(
        'Title: ',
        validators=[DataRequired()]
    )
    runtime = IntegerField(
        'Runtime (sec): ',
        validators=[DataRequired(), NumberRange(min=0)]
    )