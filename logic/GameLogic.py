# -*- coding: utf-8 -*-

from logic.PlayerManager import PlayerManager
class GameLogic(object):
	def __init__(self):
		self.player_mgr = PlayerManager()

	def destroy(self):
		self.player_mgr.destroy()

	def tick(self):
		self.player_mgr.tick()
