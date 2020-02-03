from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/download', methods=['GET', 'POST'])
def download():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Need download info')
	return render_template('download.html', title='Download')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form)