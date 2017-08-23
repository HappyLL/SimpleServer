# -*- coding: utf-8 -*-

import inspect

def component_host(kclass):
	kclass.__component_flag__ = True
	kclass._add_component = classmethod(_add_component)
	kclass._del_component = classmethod(_del_component)
	kclass._call_component = _call_component
	kclass.__components__ = []
	for index, base in enumerate(kclass.__bases__):
		components = getattr(base, '__components__', None)
		if components:
			kclass.__components__.append(components)

def _add_component(kclass, component):
	# .1 判断component 是否是已有component的子类
	for i, base in enumerate(kclass.__components__):
		if issubclass(component, base):
			kclass.__components__[i] = component
			break
	else:
		kclass.__components__.append(component)
	# .2 复制所有的func(包括基类中的)
	copies_func = inspect.getmembers(component, inspect.ismethod)
	for ind, func_info in enumerate(copies_func):
		func_name = func_info[0]
		if str.startswith(func_name, "__") or str.endswith(func_name, "__"):
			continue
		im_func = func_info[1].im_func
		setattr(kclass, func_name, im_func)
	# .3 复制所有的member(包括基类中)
	copies_mems = inspect.getmembers(component, is_user_type)
	for ind, member_info in enumerate(copies_mems):
		if str.startswith(member_info[0], "__") or str.endswith(member_info[0], "__"):
			continue
		setattr(kclass, member_info[0], member_info[1])

def _del_component(kclass, component):
	if component not in kclass.__components__:
		return
	kclass.__components__.remove(component)
	copies_func = inspect.getmembers(component, inspect.ismethod)
	for ind, func_info in enumerate(copies_func):
		func_name = func_info[0]
		if str.startswith(func_name, "__") or str.endswith(func_name, "__"):
			continue
		delattr(kclass, func_name)

	copies_mems = inspect.getmembers(component, is_user_type)
	for ind, member_info in enumerate(copies_mems):
		if str.startswith(member_info[0], "__") or str.endswith(member_info[0], "__"):
			continue
		delattr(kclass, member_info[0])

# 调用组件特有方法(__%s__component形式,来控制组件生命周期等)
def _call_component(self, func_name, *args, **kwargs):
	func_name = "_%s_component"%(func_name)
	print 'func_name is ',func_name
	for _, component in enumerate(self.__components__):
		#print dir(component)
		func = getattr(component, func_name, None)
		func and func.im_func(self, *args, **kwargs)

user_types = [int, str, tuple, list, dict]
def is_user_type(member):
	return type(member) in user_types

# 组件装饰器
def component_cls(*components):
	def _component(kclass):
		if not getattr(kclass, '__component_flag__', None):
			component_host(kclass)
		print 'dir kclass is ', dir(kclass)
		for _, component in enumerate(components):
			# 判断是模块还是类
			if inspect.ismodule(component):
				cls_members = inspect.getmembers(component, inspect.isclass)
				for index, cls_info in enumerate(cls_members):
					kclass._add_component(cls_info[1])
			elif inspect.isclass(component):
				kclass._add_component(component)
		return kclass
	return _component