#!/usr/bin/python
# -*- coding: utf-8 -*-
#SQTSignal.py
import baseSignal

class CSQTSignal(baseSignal.CBaseSingal):
	#------------------------------
	#继承重载函数
	#------------------------------
	#自定义初始化函数
	def customInit(self):
		self.name = "SQTSignal"
	#行情数据触发函数
	def onRtnMarketData(self, data):
		pass
	#逐笔成交触发函数
	def onRtnTradeSettlement(self, data):
		pass
	#买一队列触发函数
	def onRtnOrderQueue(self, data):
		pass
	def dayBegin(self):
		pass
	def dayEnd(self):
		pass
	#自动保存缓存触发函数
	def autosaveCache(self):
		#self.saveCache(data = self.data)
		pass