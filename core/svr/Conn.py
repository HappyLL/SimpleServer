# -*- coding: utf-8 -*-

import threading

lock = threading.Lock()

class Config(object):
	pass

# 连接对象
class Conn(object):
	def __init__(self, conn_id):
		self._flag_used = False
		self._flag_writeable = False
		self._conn_id = conn_id
		self._socket = None

	def recv_dat(self, dat):
		pass

	def send_dat(self):
		pass

	@property
	def used(self):
		return self._flag_used

	@used.setter
	def used(self, value):
		self._flag_used = value

	@property
	def writeable(self):
		return self._flag_writeable

	@writeable.setter
	def writeable(self, value):
		self._flag_writeable =value

	@property
	def connsk(self):
		return self._socket

	@connsk.setter
	def connsk(self, value):
		self._socket = value

	def close_conn(self):
		self._socket = None
		self._flag_writeable = False
		self.used = False
