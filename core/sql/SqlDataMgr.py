# -*- coding: utf-8 -*-

from system.decorator.Singleton import singleton
import mysql.connector
import re

class Config(object):
	sql_ip = '127.0.0.1'
	sql_port = 3306
	sql_user = 'root'
	sql_pwq = '' # mac下没有密码
	sql_db_name = 'game'

	tb_player = 'player'
	tb_user = 'user'

@singleton
class SqlDataMgr(object):
	def __init__(self, connect_info=None):
		self._init_connect_info(connect_info)
		self._conn = None
		self._cursor = None

	def _init_connect_info(self, connect_info):
		connect_info = connect_info or {}
		self._sql_ip = connect_info.get('sql_ip') or Config.sql_ip
		self._sql_port = connect_info.get('sql_port') or Config.sql_port
		self._sql_user = connect_info.get('sql_user') or Config.sql_user
		self._sql_pwq = connect_info.get('sql_pwq') or Config.sql_pwq
		self._sql_db_name = connect_info.get('sql_db_name') or Config.sql_db_name

	# 连接
	def connect(self):
		if self._conn:
			print 'the db is connected not connect angain'
			return
		try:
			self._conn = mysql.connector.connect(user=self._sql_user, password=self._sql_pwq, database=self._sql_db_name)
		except Exception:
			self._conn = None
			print 'connect db error'
		else:
			print 'connected db success'

	# 关闭
	def shutdown(self):
		if self._conn is None:
			print 'the db is disconnected not disconnect angain'
			return
		try:
			self._conn.close()
		except Exception:
			print 'disconnect db error'
		else:
			self._conn = None
			print 'close db success'

	#注册
	def register(self, player_id, pwd):
		if self._conn is None:
			return
		if not self._check_register(player_id):
			print 'error player_id'
			return
		if not self._check_wd_safe(pwd):
			print 'error word error'
			return
		self._insert_db_user(player_id, pwd)


	# 判断能否注册
	def _check_register(self, player_id):
		if self._check_wd_safe(player_id) and self._check_not_repeat_id(player_id):
			return True
		return False

	def _check_wd_safe(self, wd):
		return True

	def _check_not_repeat_id(self, player_id):
		ret = self._search_db_by_id(player_id, Config.tb_user)
		print '_check_not_repeat_id ', ret
		return ret is None or len(ret) == 0

	def _search_db_by_id(self, player_id, tb_nm):
		_sql = 'select * from %s where id = %s'%(tb_nm, player_id)
		print 'id_search ', _sql
		self._cursor = self._conn.cursor()
		self._cursor.execute(_sql)
		ret = self._cursor.fetchall()
		self._cursor.close()
		self._cursor = None
		return ret

	def _insert_db_user(self, player_id, pwd):
		_sql = 'insert into user (id, pw) values (%s, %s)'%(player_id, pwd)
		print 'user_insert', _sql
		self._cursor = self._conn.cursor()
		self._cursor.execute(_sql)
		self._conn.commit()
		self._cursor.close()
		self._cursor = None
