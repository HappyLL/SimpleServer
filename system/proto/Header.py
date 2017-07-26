# -*- coding: utf-8 -*-

import struct
import string

class Config(object):
	HEADER_FORMAT = '='
	CHAR_FOR_LEN = 'I'

# 具体协议的类
class Header(object):
	def __init__(self, hid):
		self._hid = hid
		self._valnm_list = []
		self._hfmt = Config.HEADER_FORMAT + 'H'
		self._bfmt = ''

	def header_encode(self):
		head_dat = self._get_en_head()
		bin_dat = self._get_en_bin()
		enc_dat = head_dat + bin_dat
		return enc_dat

	def header_decode(self, dat):
		wsz = struct.calcsize(self._hfmt)
		tu_hid = struct.unpack(self._hfmt, dat[0:wsz])
		hid = tu_hid[0]
		if self._hid != hid:
			raise ValueError('the hid is error')
		self._decode_val(dat[wsz:])

	def _add_val(self, val_nm, val, val_type):
		if val_nm in self._valnm_list:
			print 'val_nm is same in nmlist'
			return
		self.__setattr__(val_nm, val)
		val_type = val_type.strip()
		if val_type == 's':
			# 空值对象用来记录字符串长度
			self._valnm_list.append(None)
			self._bfmt += Config.CHAR_FOR_LEN
			self._bfmt += '%ds'
		else:
			self._bfmt += val_type

		self._valnm_list.append(val_nm)

	def _del_val(self, val_nm):
		if not (val_nm in self._valnm_list):
			print 'val nm is not in nmlist'
			return
		self.__delattr__(val_nm)
		self._valnm_list.remove(val_nm)

	def __getattr__(self, key):
		if not (key in self._valnm_list):
			raise ValueError('key error')
		return self.__dict__[key]

	def _get_en_head(self):
		return struct.pack(self._hfmt, self._hid)

	def _get_en_bin(self):
		bin_fmt, bin_values = self._get_encode_bin()
		return struct.pack(Config.HEADER_FORMAT + bin_fmt, *bin_values)

	def _get_decode_bin_format(self, dat):
		bin_fmt = self._bfmt
		cnt = string.count(bin_fmt, '%')
		ed = 0
		fmt_ln = Config.HEADER_FORMAT + Config.CHAR_FOR_LEN
		offest = struct.calcsize(fmt_ln)
		ln_dat = len(dat)
		if cnt == 0:
			return bin_fmt
		ret = []
		for i in range(cnt):
			ind = string.index(bin_fmt, '%')
			ed = ind
			wsz = struct.calcsize(Config.HEADER_FORMAT + bin_fmt[0:ed])
			if ln_dat < wsz:
				raise ValueError('_get_decode_bin_format error')
			wln_st = wsz - offest
			tu_str = struct.unpack(fmt_ln, dat[wln_st:wsz])
			ret.append(tu_str[0])
			ed = ed + len('%ds')
			wsz = wsz + tu_str[0]
			bin_fmt = bin_fmt[ed:]
			dat = dat[wsz:]
		return self._bfmt%(tuple(ret))

	def _get_encode_bin(self):
		ret = []
		bin_fmt = self._bfmt
		str_len_list = []
		last_nam = None
		for index in range(len(self._valnm_list)):
			val_nam = self._valnm_list[index]
			if not val_nam:
				last_nam = val_nam
				continue
			val = self.__getattr__(val_nam)
			if not last_nam:
				ln_nm = len(val)
				str_len_list.append(ln_nm)
				ret.append(ln_nm)
			ret.append(val)
			last_nam = val_nam
		return bin_fmt%tuple(str_len_list), ret

	def _decode_val(self, dat):
		bin_format = self._get_decode_bin_format(dat)
		print 'bin_format is ', bin_format
		de_vals = struct.unpack(Config.HEADER_FORMAT + bin_format, dat)
		print 'header de_val is ',de_vals
		ln_nm = len(self._valnm_list)
		if ln_nm != len(de_vals):
			raise ValueError('decode val error len not equal')

		for index in range(ln_nm):
			if not self._valnm_list[index]:
				continue
			self.__setattr__(self._valnm_list[index], de_vals[index])

