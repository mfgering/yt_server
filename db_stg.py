import sqlite3
from datetime import datetime
from time import strftime


class Stg(object):

	def __init__(self):
		super().__init__()
		self.conn = None

	def get_connection(self):
		if self.conn is None:
			self.conn = sqlite3.connect('yt_server.db')
			self.init_tables()
		return self.conn

	def init_tables(self):
		query = '''SELECT count(*) FROM sqlite_master WHERE type='table' AND name=:table_name;'''
		cur = self.get_connection().execute(query, {'table_name': 'downloads'})
		results = cur.fetchone()
		if results[0] == 0:
			cur.execute('''create table downloads(
				queued_time text, 
				run_time text, 
				done_time text,
				url text, 
				title text)''')
		cur.close()

	def enqueue(self, url, title):
		conn = self.get_connection()
		sql = ''' insert into downloads(queued_time, url, title) values(:qtime, :url, :title)'''
		cur = conn.execute(sql, {'qtime': self._now_str(), 'url': url, 'title': title})
		conn.commit()
		cur.close()
		return cur.lastrowid

	def start_run(self, stg_id, title):
		conn = self.get_connection()
		sql = ''' update downloads set run_time = :rtime, title = :title where rowid = :stg_id;'''
		cur = conn.execute(sql, {'rtime': self._now_str(), 'stg_id': stg_id, 'title': title})
		if cur.rowcount != 1:
			raise Exception("No row found for "+stg_id)
		conn.commit()
		cur.close()
	
	def done(self, stg_id):
		conn = self.get_connection()
		sql = ''' update downloads set 
			done_time = :dtime
			where rowid = :stg_id '''
		parms = {'dtime': self._now_str(), 'stg_id': stg_id}
		cur = conn.execute(sql,parms)
		if cur.rowcount != 1:
			raise Exception("No row found for "+stg_id)
		conn.commit()
		cur.close()


	def _now_str(self):
		now = datetime.now()
		return now.strftime("%m/%d/%y %H:%M:%S")

'''
x = Stg()
id = x.enqueue('my url')
z = x.start_run(id)
w = x.done(id, "my file", 323)
y = Stg()
'''