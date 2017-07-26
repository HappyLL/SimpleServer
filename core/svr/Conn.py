# -*- coding: utf-8 -*-

from system.proto import Proto
import time
from system.event import EventDispatcher
from system.event import EventConst
#from system.event import NetEventDispatcher

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
		self._is_new_player = False
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

	@property
	def is_new_player(self):
		return self._is_new_player

	@is_new_player.setter
	def is_new_player(self, value):
		self._is_new_player = value
		if value is True:
			EventDispatcher.dispatch_event(EventConst.EID_CREATE_NEW_PLAYER, self)

	def close_conn(self):
		self._socket = None
		self._flag_writeable = False
		self.used = False
		self._recvbuff = ''
		self._sendbuff = ''
		self._is_new_player = False
		EventDispatcher.dispatch_event(EventConst.EID_DESTROY_NEW_PLAYER, self)

	def tick(self):
		self._handle_msg()

	def _handle_msg(self):
		ret = self.get_proto()
		if not ret or len(ret) == 0:
			return
		hid = ret[0]
		buff = ret[1]
		EventDispatcher.dispatch_event(hid, buff)