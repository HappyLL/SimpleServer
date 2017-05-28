# -*- coding: utf-8 -*-

from core.svr.ServNet import SevrNet

class Server(object):
	def __init__(self):
		pass

	def svr_start(self):
		self._init_net_mod()

	def svr_end(self):
		self._netSvr.end_svr_net()
		self._netSvr = None

	# 初始化网络连接模块
	def _init_net_mod(self):
		self._netSvr = SevrNet()
		self._netSvr.init_svr_net()

	def tick(self):
		self._netSvr.tick()