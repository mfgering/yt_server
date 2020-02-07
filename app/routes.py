from flask import render_template, flash, redirect
import downloader
from app import app
from app.forms import LoginForm, DownloadForm
#TODO: Add link for download log details

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/download', methods=['GET', 'POST'])
def download():
	form = DownloadForm()
	if form.validate_on_submit():
		msg = downloader.Downloader.submit_download(form)
		if msg is not None:
			flash(msg)
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

@app.route('/status', methods=['GET'])
def status():
	context = {}
	context['done'] = _get_thread_status(downloader.Downloader.Done)
	context['running'] = _get_thread_status(downloader.Downloader.Running)
	context['queued'] = _get_thread_status(downloader.Downloader.Queue)
	return render_template("status.html", title="Status", context=context)

def _get_thread_status(items):
	"""
	{'_eta_str': '02:47:10', '_percent_str': '  0.0%', '_speed_str': '155.37KiB/s', 
	'_total_bytes_estimate_str': '34.80MiB', 'downloaded_bytes': 1024, 
	'elapsed': 0.2814369201660156, 'eta': 10030, 'filename': '//alpha.dawson/test...ation.mp4', 
	'fragment_count': 101, 'fragment_index': 0, 'speed': 159096.43265668987, 'status': 
	'downloading', 'tmpfilename': '//alpha.dawson/test....mp4.part', 
	'total_bytes_estimate': 36494936.0}
	"""
	result_data = []
	for thrd in items:
		j_data = {"url": thrd.url, "log": thrd.get_log()}
		if thrd.progress is not None:
			j_data['ETA'] = thrd.progress.get('_eta_str', '')
			j_data['Percent'] = thrd.progress.get('_percent_str', '')
			j_data['Status'] = thrd.progress.get('status', '')
			j_data['Filename'] = thrd.progress.get('filename', '')
			j_data['Total Bytes'] = sizeof_fmt(thrd.progress.get('total_bytes', '0'), '')
			j_data['Speed'] = thrd.progress.get('_speed_str', '')
		result_data.append(j_data)
	return result_data

def sizeof_fmt(num, suffix='o'):
	"""Readable file size

	:param num: Bytes value
	:type num: int
	:param suffix: Unit suffix (optional) default = o
	:type suffix: str
	:rtype: str
	"""
	for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
		if abs(num) < 1024.0:
			return "%3.1f %s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)
