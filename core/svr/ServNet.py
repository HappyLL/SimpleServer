# -*- coding: utf-8 -*-

from core.svr.Conn import Conn
import socket

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
		while True:
			sock, addr = self._socket.accept()
			print 'new client connect addr is ', (addr)
			conn = self._new_conn()
			conn.start_connect(sock , addr)

	def end_svr_net(self):
		if self._socket is None:
			print 'the socket is none'
			return
		for index in range(self._conn_num):
			if self._conn[index].used:
				self._conn[index].end_connect()
				self._conn[index].used = False
		self._conn = None
		self._conn_num = 0

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