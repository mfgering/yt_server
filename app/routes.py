from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, DownloadForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/download', methods=['GET', 'POST'])
def download():
	form = DownloadForm()
	url = None
	#x = form.validate()
	if form.validate_on_submit():
		#FIX THIS!
		flash('Need download info')
		return redirect('/download')
	if form.is_submitted():
		if form.validate():
			pass #TODO: Do the download
			print("Download it!")
		else:
			flash("There was a problem")
	return render_template('download.html', title='Download', form=form, url=url)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form)