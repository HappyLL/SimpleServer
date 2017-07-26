# -*- coding: utf-8 -*-

from core.svr.ServNet import SevrNet
from logic.PlayerManager import PlayerManager

class Server(object):
	def __init__(self):
		pass

	def svr_start(self):
		self._init_net_mod()
		self._init_logic()

	def svr_end(self):
		self._netSvr.end_svr_net()
		self._netSvr = None
		self.player_mgr.destroy()
		self.player_mgr = None

	# 初始化网络连接模块
	def _init_net_mod(self):
		self._netSvr = SevrNet()
		self._netSvr.init_svr_net()

	def _init_logic(self):
		self.player_mgr = PlayerManager()

	def tick(self):
		self._netSvr.tick()
		self.player_mgr.tick()