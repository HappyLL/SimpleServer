# -*- coding: utf-8 -*-

# 处理协议发给谁

from core.sync.NoSync import NoSync
from core.sync import SyncConst
from system.decorator.Singleton import singleton
from system.event import EventDispatcher
from system.event import EventConst
import Queue
@singleton
class ServerManger(object):
	def __init__(self):
		self.conns = []
		self.sync_mode_id = SyncConst.CONST_NO_SYNC
		self.update_cache = Queue.Queue()
		self.cache_len = 0
		self.sync_nosync = NoSync()
		self.mid2smode = {
			SyncConst.CONST_NO_SYNC: self.sync_nosync,
		}
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
				send_bytes = bytes[:]
				print 'send success all is ',conn
				from system.proto.header.MLoginSCHeader import MLoginSCHeader
				from system.proto import HeaderConst
				login = MLoginSCHeader(HeaderConst.HEADER_LOGIN_MSG_ID)
				from system.proto import Proto
				ret1, ret = Proto.decode_buffer(bytes, len(bytes))
				login.header_decode(ret1[1])
				print 'login_id is ', login.player_id
				conn.send_dat(send_bytes)

	# conn ,player_id , pos_x , pos_y...
	def push_data(self, info):
		self.cache_len += 1
		self.update_cache.put(info)

	def pop_data(self):
		if self.cache_len == 0:
			return None
		self.cache_len -= 1
		self.update_cache.get()

	def tick(self):
		sync_model = self.mid2smode.get(self.sync_mode_id)
		if not sync_model:
			return
		sync_model.tick()
