# -*- coding: utf-8 -*-

from system.event import EventDispatcher
from system.proto import HeaderConst


class Player():
	def __init__(self, conn):
		self._conn = conn
		self.register_msg()

	def register_msg(self):
		EventDispatcher.add_event_listener(self, HeaderConst.HEADER_LOGIN_MSG_ID, self._login_success)

	def _login_success(self, bytes):
		from system.proto.header.MLoginSCHeader import MLoginSCHeader
		login = MLoginSCHeader(HeaderConst.HEADER_LOGIN_MSG_ID)
		login.header_decode(bytes)
		print login
		#test
		s = ''
		for index in xrange(10000):
			s += 'i'
		import struct
		self._conn.send_dat(struct.pack('=I10000s', 10000, s))

	def cancel_msg(self):
		EventDispatcher.remove_event_listener(self)

	def tick(self):
		pass

	def destroy(self):
		self.cancel_msg()