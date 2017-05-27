# -*- coding: utf-8 -*-

from core.svr.Conn import Conn
import socket
import threading

lock = threading.Lock()

class Config(object):
	default_ip = '127.0.0.1'
	default_port = 8888
	conn_max_num = 200

class SevrNet(object):

	def __init__(self):
		self._conn = []
		self._socket = None
		self._conn_num = 0

	def init_svr_net(self, ip=Config.default_ip, port=Config.default_port):
		if self._socket:
			print 'socket init again'
			return
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.bind((ip, port))
		self._socket.listen(Config.conn_max_num)

	def start_svr_net(self):
		if self._socket is None:
			print 'the socket is none'
			return
		# svr不能写成while True 模式 不然 svrnet 只能处理连接信息了
		# while True:
		# 	sock, addr = self._socket.accept()
		# 	print 'new client connect addr is ', (addr)
		# 	conn = self._new_conn()
		# 	conn.start_recv(sock, addr)
		self._begin_accept()

	def end_svr_net(self):
		if self._socket is None:
			print 'the socket is none'
			return
		for index in range(self._conn_num):
			if self._conn[index].used:
				self._conn[index].end_recv()
				self._conn[index].used = False
		self._conn = None
		self._conn_num = 0

	def _begin_accept(self):
		td = threading.Thread(target=self._cb_accepted)
		td.start()

	def _cb_accepted(self):
		# 操作的self._socket
		sock, addr = self._socket.accept()
		print 'new client connect addr is ', (addr)
		conn = self._new_conn()
		conn.start_recv(sock, addr)
		self._begin_accept()

	def _new_conn(self):
		self._conn_num += 1
		if self._conn_num >= Config.conn_max_num:
			print "the connector is up to max_num"
			return
		conn_len = len(self._conn)
		for index in range(conn_len):
			if not self._conn[index].used:
				return self._conn[index]
		new_conn = Conn(self._conn_num)
		return new_conn
