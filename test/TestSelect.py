# -*- coding: utf-8 -*-

# IO-select模型

import select
import socket

class SelectSvr(object):
	def __init__(self):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.bind(('127.0.0.1', 8181))
		self._socket.listen(5)
		self._socket.setblocking(False)
		self._read_list = [self._socket]
		self._write_list = []
		self._exce_list = []
		self._msg = {}

	def start_svr(self):
		#tm_out = 20
		while len(self._read_list) > 0:
			read_list, write_list, exec_list = select.select(self._read_list, self._write_list, self._exce_list)
			if not (read_list or write_list or exec_list):
				print 'time out'
				self.end_svr()
				break

			for exec_sk in exec_list:
				if exec_sk in self._read_list:
					if exec_sk == self._socket:
						self.end_svr()
						break
					self._read_list.remove(exec_sk)
				if exec_sk in self._write_list:
					self._write_list.remove(exec_sk)
				exec_sk.close()

			for read_sk in read_list:
				if read_sk == self._socket:
					# 表示新的连接
					ct, address = self._socket.accept()
					ct.setblocking(False)
					print 'new client connected ', ct, ' address is ', address
					print 'read_list ', read_list
					print 'write_list', write_list
					print 'exec_list ', exec_list
					self._read_list.append(ct)
					self._write_list.append(ct)
				else:
					try:
						# 表示有数据发过来
						dat = read_sk.recv(1024)
						self._msg[read_sk] = dat
						print 'the data is ', dat
					except:
						self._read_list.remove(read_sk)
						self._write_list.remove(read_sk)
						read_sk.close()

			for write_sk in write_list:
				dat = self._msg.get(write_sk)
				if not dat:
					continue
				del self._msg[write_sk]
				print 'the send data is ', dat
				write_sk.send(dat)

	def end_svr(self):
		self._socket.close()
		self._socket = None
		#self._read_list = None
		#self._write_list = None