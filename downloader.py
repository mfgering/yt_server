import os, sys
from config import Config
from io import StringIO
import logging
from threading import Thread
import youtube_dl.youtube_dl.YoutubeDL
import db_stg

class Downloader(object):
	Queue = []
	Running = []
	Done = []

	@classmethod
	def submit_download(cls, form):
		ytdl_opts = {}
		dl_dir = os.path.normpath(form.dl_dir.data)
		dl_patt = form.dl_patt.data
		ytdl_opts['outtmpl'] = os.path.join(dl_dir, dl_patt)
		ytdl_opts['ffmpeg_location'] = Config.FFMPEG_LOCATION
		ytdl_opts['restrictfilenames'] = Config.RESTRICT_FILENAMES
		if form.x_audio.data:
			ytdl_opts['postprocessors'] = [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}]
			#ytdl_opts["extractaudio"] = True
			#ytdl_opts["audioformat"] = "best"
		url = form.url.data
		Config.MAX_CONCURRENT_DL = form.max_dl.data
		thread = DownloadThread(Downloader.thread_callback, ytdl_opts, url)
		stg = db_stg.Stg()
		thread.stg_id = stg.enqueue(url, thread.title)
		Downloader.Queue.append(thread)
		Downloader.run_next_queued()
		msg = "Download submitted"
		return msg
	
	@classmethod
	def thread_callback(cls, thread, data=None):
		db_stg.Stg().done(thread.stg_id)
		Downloader.Running.remove(thread)
		Downloader.Done.append(thread)
		Downloader.run_next_queued()

	@classmethod
	def run_next_queued(cls):
		stg = db_stg.Stg()
		while(len(Downloader.Queue) > 0 and (len(Downloader.Running) < Config.MAX_CONCURRENT_DL or Config.MAX_CONCURRENT_DL < 0)):
			thread = Downloader.Queue.pop()
			stg.start_run(thread.stg_id, thread.title)
			Downloader.Running.append(thread)
			thread.start()

class DownloadThread(Thread):
	def __init__(self, callback, ytdl_opts, url):
		super().__init__()
		self.callback = callback
		self.progress = None
		self.logger = logging.getLogger(self.getName())
		self.log_stream = StringIO()
		handler = logging.StreamHandler(stream=self.log_stream)
		self.logger.addHandler(handler)
		self.logger.setLevel(logging.DEBUG)
		opts = ytdl_opts.copy()
		opts['logger'] = self.logger
		ytdl = youtube_dl.youtube_dl.YoutubeDL(opts)
		info = ytdl.extract_info(url, download=False)
		self.title = '*** unknown ***'
		if 'title' in info:
			self.title = info['title']
		ytdl.add_progress_hook(self.progress_callback)
		self.ytdl = ytdl
		self.url = url
		self.log = ""
		self.stg_id = None

	def get_logger(self):
		return self.logger

	def run(self):
		try:
			self.ytdl.download([self.url])
			print("ytdl done")
		except Exception as exc:
			print(str(exc))
		self.log = self.log_stream.getvalue()
		self.log_stream.close()
		self.callback(thread=self, data={})

	def progress_callback(self, data):
		assert(data is not None)
		self.progress = data

	def get_log(self):
		return self.log
