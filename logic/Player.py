# -*- coding: utf-8 -*-

from system.event import EventDispatcher
from system.proto import HeaderConst
from logic.ServerManager import ServerManger


class Player():
	def __init__(self, conn):
		self._conn = conn
		self._init_player_info()
		self.register_msg()
		self._login_success()

	def _init_player_info(self):
		self._player_id = self._conn.conn_id
		self._name = ''
		import random
		self._pos_x = random.randint(-16, 16)
		self._pos_y = random.randint(-10, 10)
		self._v_x = 0
		self._v_y = 0

	def register_msg(self):
		pass
		#EventDispatcher.add_notify_event_listener(self._conn, self, HeaderConst.HEADER_LOGIN_MSG_ID, self._login_success)

	def _login_success(self):
		from system.proto.header.MLoginSCHeader import MLoginSCHeader
		login = MLoginSCHeader(HeaderConst.HEADER_LOGIN_MSG_ID)
		login.player_id = 10000 # self._player_id
		login.pos_x = self._pos_x
		login.pos_y = self._pos_y
		from system.proto import Proto
		ret_bytes = login.header_encode()
		bytes_len = len(ret_bytes)
		ServerManger().send_proto_to_all(Proto.encode_buffer(ret_bytes, bytes_len))

	def cancel_msg(self):
		EventDispatcher.remove_event_listener(self)

	def tick(self):
		pass

	def destroy(self):
		self.cancel_msg()
