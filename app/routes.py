from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, DownloadForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/download', methods=['GET', 'POST'])
def download():
	form = DownloadForm()
	url = None
	if form.validate_on_submit():
		#TODO: Download
		return redirect('/download')
	if len(form.errors) > 0:
		flash("Please fix the problems and try again.")
	return render_template('download.html', title='Download', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form)