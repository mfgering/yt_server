from pathlib import Path
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL, ValidationError

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class DownloadForm(FlaskForm):
	url = StringField('URL', validators=[DataRequired(message='URL is needed'), URL(message="Invalid URL")])
	dl_dir = StringField('Download directory', validators=[DataRequired(message='A directory name is needed')])
	dl_patt = StringField('Download pattern', validators=[DataRequired(message='A pattern is needed')])
	x_audio = BooleanField("Audio only")
	submit = SubmitField('Submit')

	@staticmethod
	def validate_dl_dir(form, field):
		path1 = Path(field.data)
		if path1.is_file():
			raise ValidationError("Should be a directory, not a file.")
		if path1.is_dir():
			#TODO: Can write file in the directory?
			return
		try:
			path1.mkdir(parents=True, exist_ok=False)
		except Exception as exc:
			raise ValidationError("Could not create the directory: "+str(exc))
