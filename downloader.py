from config import Config
from io import StringIO
from threading import Thread
import youtube_dl.youtube_dl.YoutubeDL

class Downloader(object):
    Queue = []
    Running = []

    @classmethod
    def submit_download(cls, form):
        ytdl_opts = {}
        ytdl_opts['outtmpl'] = Config.OUTPUT_TEMPLATE
        ytdl = youtube_dl.youtube_dl.YoutubeDL(ytdl_opts)
        url = form.url.data
        thread = DownloadThread(Downloader.thread_callback, ytdl, url)
        Downloader.Queue.append(thread)
        Downloader.run_next_queued()
        msg = None
        print("Let's download it!")
        return msg
    
    @classmethod
    def thread_callback(cls, thread, data=None):
        Downloader.Running.remove(thread)
        Downloader.run_next_queued()

    @classmethod
    def run_next_queued(cls):
        while(len(Downloader.Queue) > 0 and len(Downloader.Running < Config.MAX_CONCURRENT_DL) or Config.MAX_CONCURRENT_DL < 0):
            thread = Downloader.Queue.pop()
            Downloader.Running.append(thread)
            thread.start()

class DownloadThread(Thread):
    def __init__(self, callback, ytdl, url):
        self.callback = callback
        self.ytdl = ytdl
        self.url = url
        self.out = StringIO()

    def start(self):
        try:
            self.ytdl.download(self.url)
        except Exception as exc:
            print(str(exc))
        self.callback(thread=self, data={})

    def write(self, string):
        