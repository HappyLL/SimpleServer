# -*- coding: utf-8 -*-

from core.svr.Conn import Conn
import socket
import select
import time

class Config(object):
	default_ip = '127.0.0.1'
	default_port = 8888
	conn_max_num = 200
	data_buffer = 1024
	# 连接最大实现
	conn_out_tm = 30

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

	# 服务器步骤: 接收数据 检测异常 测试连接
	def tick(self):
		self._process()
		#self._heat_beat()
		self._do_exec()
		self._conns_tick()

	# 处理连接
	def _process(self):
		read_lists, write_lists, exec_lists = select.select(self._read_lists, self._write_lists, self._exec_lists, 0)
		self._do_exec_sk(exec_lists)
		self._do_read_sk(read_lists)
		self._do_write_sk(write_lists)

	# 处理心跳
	def _heat_beat(self):
		now_tm = time.time()
		for index in range(len(self._conn)):
			conn = self._conn[index]
			if not conn.used:
				continue
			delta_tm = now_tm - conn.activetm
			# 超过最大时限默认断开
			if delta_tm > Config.conn_out_tm:
				print 'the index conn is disconnect', conn
				sk = conn.connsk
				self._clear_sk_lists.append(sk)

	# 处理异常sk
	def _do_exec(self):
		ln = len(self._clear_sk_lists)
		for index in range(ln):
			sk = self._clear_sk_lists[index]
			self._close_conn(sk)
			if sk in self._write_lists:
				self._write_lists.remove(sk)
			if sk in self._read_lists:
				self._read_lists.remove(sk)
			if sk in self._exec_lists:
				self._exec_lists.remove(sk)

		if ln > 0:
			self._clear_sk_lists = []

	def _conns_tick(self):
		for conn in self._conn:
			if conn.used:
				conn.tick()

	def _init_data(self):
		self._sk2conn = {}
		self._conn = []
		self._socket = None
		self._conn_num = 0
		self._read_lists = []
		self._write_lists = []
		self._exec_lists = []
		self._clear_sk_lists = []

	def _clear_data(self):
		self._sk2conn = None
		self._conn = None
		self._socket = None
		self._conn_num = 0
		self._read_lists = None
		self._write_lists = None
		self._exec_lists = None
		self._clear_sk_lists = None

	def _do_exec_sk(self, exec_lists):
		if len(exec_lists) > 0:
			print 'exe_lists ', exec_lists
		for exec_sk in exec_lists:
			if exec_sk == self._socket:
				self.end_svr_net()
				raise ValueError('svr net socket exception')
		self._clear_sk_lists += exec_lists

	def _do_read_sk(self, read_lists):
		for read_sk in read_lists:
			# 表示有新的连接
			if read_sk == self._socket:
				sk, address = self._socket.accept()
				print 'new client connected address is ', address
				self._read_lists.append(sk)
				self._write_lists.append(sk)
				self._exec_lists.append(sk)
				sk.setblocking(False)
				conn = self._new_conn()
				self._sk2conn[sk] = conn
				conn.used = True
				conn.connsk = sk
				conn.is_new_player = True
			# 表示当前其他sk有数据
			else:
				try:
					dat = read_sk.recv(Config.data_buffer)
					if dat is None or len(dat) == 0:
						continue
					#print 'dat is ', dat
					conn = self._sk2conn.get(read_sk)
					if conn is None:
						print 'the conn is none'
					else:
						conn.recv_dat(dat)
				except Exception, e:
					print 'exception is', e
					self._clear_sk_lists.append(read_sk)

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
		for index in xrange(conn_len):
			if not self._conn[index].used:
				return self._conn[index]
		new_conn = Conn(self._conn_num)
		self._conn.append(new_conn)
		return new_conn

	def _close_conn(self, sk):
		conn = self._sk2conn.get(sk)
		if not conn:
			return
		print 'close conn is ', conn
		conn.close_conn()
		sk.close()

	def _close_all_conn(self):
		if self._sk2conn is None:
			return
		for sk in self._sk2conn:
			self._close_conn(sk)
		self._socket.close()

	def _dis_connect_sk(self, sk):
		self._close_conn(sk)
		del self._sk2conn[sk]
		self._read_lists.remove(sk)
