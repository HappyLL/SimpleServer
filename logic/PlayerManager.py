# -*- coding: utf-8 -*-
from system.event import EventDispatcher
from system.event import EventConst

class PlayerManager():
	def __init__(self):
		self.players = {}
		self.dirty_tick = True
		self.register_msg()

	def register_msg(self):
		EventDispatcher.add_event_listener(self, EventConst.EID_CREATE_NEW_PLAYER, self._create_new_player)
		EventDispatcher.add_event_listener(self, EventConst.EID_DESTROY_NEW_PLAYER, self._destory_new_player)

	def cancel_msg(self):
		EventDispatcher.remove_event_listener(self)

	def _create_new_player(self, conn):
		print '_create_new_player ',conn
		from logic.Player import Player
		self.players[conn] = (Player(conn))

	def _destory_new_player(self, conn):
		if conn not in self.players:
			return
		del self.players[conn]

	def tick(self):
		if not self.dirty_tick:
			return
		for _, player in self.players.iteritems():
			player.tick()

	def destroy(self):
		self.cancel_msg()
		for player in self.players:
			player.destroy()
		self.players = None
		self.dirty_tick = False