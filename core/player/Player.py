# -*- coding: utf-8 -*-

from data.sql_data.PlayerData import PlayerData


# 角色数据
class Player(object):
	def __init__(self, player_id, player_data):
		self._player_id = player_id
		self._player_data = player_data