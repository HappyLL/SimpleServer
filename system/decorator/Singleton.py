# -*- coding: utf-8 -*-


# 单例装饰器
def singleton(kclass):
	instance = {}

	def get_instance():
		if kclass not in instance:
			instance[kclass] = kclass()
		return instance[kclass]

	return get_instance
