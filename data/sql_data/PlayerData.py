# -*- coding: utf-8 -*-

from data.CodeData import CodeData


# 人物数据
class PlayerData(CodeData):
	def __init__(self):
		self._score = 0
		self._name = '李'

	def init_from_dict(self, dt):
		if dt is None:
			return
		print 'init from dict ', dt
		self._score = dt.get('_score')
		self._name = dt.get('_name')
