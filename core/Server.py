# -*- coding: utf-8 -*-

from core.svr.ServNet import SevrNet
from logic.GameLogic import GameLogic
from logic.ServerManager import ServerManger

class Server(object):
	def __init__(self):
		pass

	def svr_start(self):
		self._init_net_mod()
		self._init_logic()

	def svr_end(self):
		self._netSvr.end_svr_net()
		self._netSvr = None
		self.game_logic.destroy()
		self.game_logic = None
		ServerManger().destroy()

	# 初始化网络连接模块
	def _init_net_mod(self):
		self._netSvr = SevrNet()
		self._netSvr.init_svr_net()

	def _init_logic(self):
		self.game_logic = GameLogic()
		ServerManger()

	def tick(self):
		self._netSvr.tick()
		self.game_logic.tick()
		ServerManger().tick()
