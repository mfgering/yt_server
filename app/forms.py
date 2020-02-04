from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class DownloadForm(FlaskForm):
	url = StringField('URL', validators=[DataRequired(message='URL is needed'), URL(message="Invalid URL")])
	submit = SubmitField('Submit')