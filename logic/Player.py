# -*- coding: utf-8 -*-

from system.event import EventDispatcher
from system.proto import HeaderConst
from logic.ServerManager import ServerManger


class Player(object):
	def __init__(self, conn):
		self._conn = conn
		self._init_player_info()
		self.register_msg()
		#self._login_success()

	def _init_player_info(self):
		self._player_id = self._conn.conn_id
		self._name = ''
		import random
		self._pos_x = random.randint(-16, 16)
		self._pos_y = random.randint(-10, 10)
		self._v_x = 0
		self._v_y = 0

	def register_msg(self):
		EventDispatcher.add_notify_event_listener(self._conn, self, HeaderConst.HEADER_POS_MSG_ID, self._pos_changed)

	def login_success(self):
		from system.proto.header.MLoginSCHeader import MLoginSCHeader
		login = MLoginSCHeader(HeaderConst.HEADER_LOGIN_MSG_ID)
		login.player_id = self._player_id
		login.pos_x = self._pos_x
		login.pos_y = self._pos_y
		from system.proto import Proto
		ret_bytes = login.header_encode()
		bytes_len = len(ret_bytes)
		encode_bytes = Proto.encode_buffer(ret_bytes, bytes_len)
		ServerManger().send_proto_target_to_all(self._conn, encode_bytes)
		from logic.PlayerManager import PlayerManager
		players = PlayerManager().get_all_players_info()
		# 通知自己登陆成功(获取所有人的信息)
		#print 'players is ',players.itervalues()
		#print 'self is ',self
		for player in players.itervalues():
			#print 'player id is', player.player_id
			#print 'player ',player
			if player == self:
				continue
			login = MLoginSCHeader(HeaderConst.HEADER_LOGIN_MSG_ID)
			login.pos_x = player.pos_x
			login.pos_y = player.pos_y
			login.player_id = player.player_id
			ret_bytes = login.header_encode()
			ret_len = len(ret_bytes)
			bytes_len += ret_len
			encode_bytes += Proto.encode_buffer(ret_bytes, ret_len)
		self._conn.send_dat(encode_bytes)

	def cancel_msg(self):
		EventDispatcher.remove_event_listener(self)

	def tick(self):
		pass

	def destroy(self):
		self.cancel_msg()

	@property
	def pos_x(self):
		return self._pos_x

	@property
	def pos_y(self):
		return self._pos_y

	@property
	def player_id(self):
		return self._player_id

	def _pos_changed(self, bytes):
		from system.proto.header.MPosSCHeader import MPosSCHeader
		pos_header = MPosSCHeader(HeaderConst.HEADER_POS_MSG_ID)
		pos_header.header_decode(bytes)
		if pos_header.player_id != self.player_id:
			print '[Player][_pos_changed] player id not equal %d, %d'%(pos_header.player_id, self.player_id)
			return
		self._pos_x = pos_header.pos_x
		self._pos_y = pos_header.pos_y
		self._v_x = pos_header.v_x
		self._v_y = pos_header.v_y
		print 'pos_change ',self
		info = {
			'player_id': self.player_id,
			'pos_x': self.pos_x,
			'pos_y': self.pos_y,
			'v_x': self._v_x,
			'v_y': self._v_y
		}
		ServerManger().push_data(info)
