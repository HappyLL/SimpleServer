# -*- coding: utf-8 -*-

from core.svr.Conn import Conn
import socket
import select

class Config(object):
	default_ip = '127.0.0.1'
	default_port = 8888
	conn_max_num = 200
	data_buffer = 1024

class SevrNet(object):

	def __init__(self):
		self._socket = None

	def init_svr_net(self, ip=Config.default_ip, port=Config.default_port):
		if self._socket:
			print 'socket init again'
			return
		self._init_data()
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self._socket.bind((ip, port))
		self._socket.listen(Config.conn_max_num)
		self._socket.setblocking(0)
		self._read_lists.append(self._socket)

	def end_svr_net(self):
		self._close_all_conn()
		self._clear_data()

	def tick(self):
		self._process()
		if len(self._conn) > 0:
			self._conn[0].get_proto()

	def _process(self):
		read_lists, write_lists, exec_lists = select.select(self._read_lists, self._write_lists, self._exec_lists, 0)
		if self._do_exec_sk(exec_lists):
			return
		self._do_read_sk(read_lists)
		self._do_write_sk(write_lists)

	def _init_data(self):
		self._sk2conn = {}
		self._conn = []
		self._socket = None
		self._conn_num = 0
		self._read_lists = []
		self._write_lists = []
		self._exec_lists = []

	def _clear_data(self):
		self._sk2conn = None
		self._conn = None
		self._socket = None
		self._conn_num = 0
		self._read_lists = None
		self._write_lists = None
		self._exec_lists = None

	def _do_exec_sk(self, exec_lists):
		for exec_sk in exec_lists:
			if exec_sk == self._socket:
				self.end_svr_net()
				return True
			if exec_sk in self._read_lists:
				self._read_lists.remove(exec_sk)
			if exec_sk in self._write_lists:
				self._write_lists.remove(exec_sk)
			self._close_conn(exec_sk)
			del self._sk2conn[exec_sk]

	def _do_read_sk(self, read_lists):
		for read_sk in read_lists:
			# 表示有新的连接
			if read_sk == self._socket:
				sk, address = self._socket.accept()
				print 'new client connected address is ', address
				self._read_lists.append(sk)
				self._write_lists.append(sk)
				sk.setblocking(False)
				conn = self._new_conn()
				self._sk2conn[sk] = conn
				conn.used = True
				conn.connsk = sk
			# 表示当前其他sk有数据
			else:
				try:
					dat = read_sk.recv(Config.data_buffer)
					if dat is None or len(dat) == 0:
						continue
					print 'dat is ', dat
					conn = self._sk2conn.get(read_sk)
					if conn is None:
						print 'the conn is none'
					else:
						conn.recv_dat(dat)
				except Exception, e:
					print 'exception is', e
					self._close_conn(read_sk)
					del self._sk2conn[read_sk]

	def _do_write_sk(self, write_lists):
		for write_sk in write_lists:
			conn = self._sk2conn.get(write_sk)
			if conn is None:
				print '_do_write_sk conn is none'
				continue
			conn.writeable = True

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
		self._conn.append(new_conn)
		return new_conn

	def _close_conn(self, sk):
		conn = self._sk2conn.get(sk)
		if not conn:
			return
		conn.close_conn()
		sk.close()

	def _close_all_conn(self):
		if self._sk2conn is None:
			return
		for sk in self._sk2conn:
			self._close_conn(sk)
		self._socket.close()
