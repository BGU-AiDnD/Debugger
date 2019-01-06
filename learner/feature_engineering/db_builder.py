import sqlite3
from contextlib import contextmanager


class DBBuilder(object):

	def __init__(self, configuration):
		self.configuration = configuration

	def build_all_versions_db(self):
		raise NotImplementedError

	@contextmanager
	def use_sqllite(self):
		conn = sqlite3.connect(self.configuration.db_dir)
		conn.text_factory = str
		yield conn
		conn.commit()
		conn.close()
