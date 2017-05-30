# -*- coding: utf-8 -*-

from system.proto import Proto
import time

class Config(object):
	pass

# 连接对象
class Conn(object):
	def __init__(self, conn_id):
		self._flag_used = False
		self._flag_writeable = False
		self._conn_id = conn_id
		self._socket = None
		self._recvbuff = ''
		self._sendbuff = ''
		self._active_tm = time.time()

	def get_proto(self):
		ret, next_buff = Proto.decode_buffer(self._recvbuff, len(self._recvbuff))
		self._recvbuff = next_buff
		return ret

	# dat是二进制流
	def recv_dat(self, dat):
		self._recvbuff += dat
		self._active_tm = time.time()

	# dat二进制流
	def send_dat(self, dat):
		self._sendbuff += dat
		try:
			send_sz = self._socket.send(self._sendbuff)
			self._sendbuff = self._sendbuff[send_sz:]
		except Exception ,e:
			print 'exception is ', e

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

	@property
	def activetm(self):
		return self._active_tm

	@activetm.setter
	def activetm(self, value):
		self._active_tm = value


	def close_conn(self):
		self._socket = None
		self._flag_writeable = False
		self.used = False
		self._recvbuff = ''
		self._sendbuff = ''
