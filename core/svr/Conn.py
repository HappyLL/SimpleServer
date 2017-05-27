# -*- coding: utf-8 -*-

import threading

lock = threading.Lock()

class Config(object):
	pass

# 连接对象
class Conn(object):
	def __init__(self, conn_id):
		self._flag_used = False
		self._conn_id = conn_id
		self._socket = None
		self._address = None

	def start_recv(self, sk, add):
		self._socket = sk
		self._address = add

	def end_recv(self):
		lock.acquire()
		try:
			self._socket.close()
		finally:
			lock.release()
		self._address = None

	@property
	def used(self):
		return self._flag_used

	@used.setter
	def used(self, value):
		self._flag_used = value


	def _begin_recv_msg(self):
		td = threading.Thread(target=self._cb_recv_msg)
		td.start()

	def _cb_recv_msg(self):
		lock.acquire()
		try:
			self._socket.recv()
		finally:
			lock.release()
