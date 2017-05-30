# -*- coding: utf-8 -*-

from system.decorator.Singleton import singleton
import mysql.connector
from data.sql_data.PlayerData import PlayerData
from system.serializable import Serializable

class Config(object):
	sql_ip = '127.0.0.1'
	sql_port = 3306
	sql_user = 'root'
	# mac下没有密码
	sql_pwq = '123456'
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

	# 注册
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
		self._create_player_data(player_id)

	# 登录校验
	def check_sign(self, player_id, pwd):
		if self._conn is None:
			return
		if not self._check_wd_safe(player_id) or not self._check_wd_safe(pwd):
			print 'player id or pwd id is not safe'
			return False
		ret = self._search_db_by_id(player_id, Config.tb_user)
		if ret is None or len(ret) == 0:
			print 'the user not exist'
			return False
		tmp_pwd = ret[0][1]
		if not tmp_pwd == pwd:
			print 'sign failed, db_pwd is %s pwd is %s', tmp_pwd, pwd
			return False
		return player_id, self._get_player_data(player_id)

	# 存储玩家信息
	def save_player_info(self, player_id, player_data):
		self._update_db_player(player_id, player_data)

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
		_sql = "select * from %s where id = '%s'"%(tb_nm, player_id)
		print 'id_search ', _sql
		self._cursor = self._conn.cursor()
		self._cursor.execute(_sql)
		ret = self._cursor.fetchall()
		self._cursor.close()
		self._cursor = None
		return ret

	def _upins_common(self, sql):
		self._cursor = self._conn.cursor()
		self._cursor.execute(sql)
		self._conn.commit()
		self._cursor.close()
		self._cursor = None

	def _insert_db_user(self, player_id, pwd):
		_sql = 'insert into user (id, pw) values (\'%s\', \'%s\')'%(player_id, pwd)
		print 'user_insert', _sql
		self._upins_common(_sql)

	def _insert_db_player(self, player_id, jstr):
		_sql = 'insert into player (id, data) values (\'%s\', \'%s\')'%(player_id, jstr)
		print 'player_insert', _sql
		self._upins_common(_sql)

	def _update_db_player(self, player_id, player_data):
		if player_id is None or player_data is None:
			raise ValueError('info is None')
		jstr = str(Serializable.encode_obj2json(player_data))
		_sql = "update player set data = '%s' where id = '%s'"%(jstr, player_id)
		self._upins_common(_sql)

	# 创建player_data(在注册成功之后)
	def _create_player_data(self, player_id):
		player_data = PlayerData()
		jstr = str(Serializable.encode_obj2json(player_data))
		self._insert_db_player(player_id, jstr)

	# 登录成功后获取角色数据
	def _get_player_data(self, player_id):
		ret = self._search_db_by_id(player_id, Config.tb_player)
		if ret is None or len(ret) == 0:
			print 'can not read player data'
			return None
		play_data = Serializable.decode_json2obj(ret[0][1])
		return play_data
