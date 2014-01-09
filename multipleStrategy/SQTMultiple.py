#!/usr/bin/python
# -*- coding: utf-8 -*-
#SQTMultiple.py
import baseMultiple

class CSQTMultiple(baseMultiple.CBaseMultiple):
	#------------------------------
	#继承重载函数
	#------------------------------
	#自定义初始化函数
	def customInit(self):
		self.name = "SQTMultiple"
	#行情数据触发函数
	def onRtnMarketData(self, data):
		pass
	def dayBegin(self):
		pass
	def dayEnd(self):
		pass
	#自动保存缓存触发函数
	def autosaveCache(self):
		#self.saveCache(data = self.data)
		pass