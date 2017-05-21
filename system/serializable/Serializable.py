# -*- coding: utf-8 -*-

import json


def encode_obj2json(obj):
	dt = {}
	dt['kclass'] = str(obj.__class__.__name__)
	dt['kmodule'] = str(obj.__module__)
	dt.update(obj.__dict__)
	encode_json = json.dumps(obj, default=lambda obj: dt, ensure_ascii=False)
	return encode_json

def decode_json2obj(jstr):
	dt = json.loads(jstr)
	kclass_name = dt.get('kclass')
	kmodule = dt.get('kmodule')
	if kclass_name is None or kmodule is None:
		raise ValueError('decode 2 obj is error')
	mod = __import__(kmodule, globals(), locals(), [kclass_name])
	kclass = getattr(mod, kclass_name)
	if kclass is None:
		raise ValueError('decode 2 obj mod not had kclass %s'%str(kclass))
	obj = kclass()
	obj.init_from_dict(dt)
	return obj