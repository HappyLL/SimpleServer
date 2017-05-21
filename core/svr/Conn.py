# -*- coding: utf-8 -*-

import threading

lock = threading.Lock()

# 连接对象
class Conn(object):
	def __init__(self, conn_id):
		self._flag_used = False
		self._conn_id = conn_id
		self._socket = None
		self._address = None

	def start_connect(self, sk, add):
		self._socket = sk
		self._address = add
		self._thread = threading.Thread(target=self._tcp_link)
		self._thread.start()

	def end_connect(self):
		self._socket.close()
		self._address = None

	@property
	def used(self):
		return self._flag_used

	@used.setter
	def used(self, value):
		self._flag_used = value

	def _tcp_link(self):
		lock.acquire()
		try:

		finally:
			lock.release()
