# -*- coding: utf-8 -*-

# 处理协议发给谁

from core.sync.NoSync import NoSync
from system.decorator.Singleton import singleton
from system.event import EventDispatcher
from system.event import EventConst

@singleton
class ServerManger(object):
	def __init__(self):
		self.conns = []
		self.sync_nosync = NoSync()
		self.register_msg()

	def register_msg(self):
		EventDispatcher.add_event_listener(self, EventConst.EID_CREATE_NEW_PLAYER, self._new_conn)
		EventDispatcher.add_event_listener(self, EventConst.EID_DESTROY_NEW_PLAYER, self._destory_conn)

	def destroy_msg(self):
		EventDispatcher.remove_event_listener(self)

	def _new_conn(self, conn):
		print '_new_conn is ', conn
		if conn in self.conns:
			return
		self.conns.append(conn)

	def _destory_conn(self, conn):
		if conn not in self.conns:
			return
		self.conns.remove(conn)

	def destroy(self):
		self.cancel_msg()

	def send_proto_to_all(self, bytes):
		print 'conns is ', self.conns
		for conn in self.conns:
			conn.send_dat(bytes)

	def send_proto_target_to_all(self, player_conn, bytes):
		for conn in self.conns:
			if conn != player_conn:
				conn.send_dat(bytes)
