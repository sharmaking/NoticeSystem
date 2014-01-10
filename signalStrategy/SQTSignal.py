#!/usr/bin/python
# -*- coding: utf-8 -*-
#SQTSignal.py
import baseSignal
import copy

class CSQTSignal(baseSignal.CBaseSingal):
	#------------------------------
	#继承重载函数
	#------------------------------
	#自定义初始化函数
	def customInit(self):
		self.name = "SQTSignal"
		self.timeSharingDataList = []	#分时时间数据
	#行情数据触发函数
	def onRtnMarketData(self, data):
		self.getTimeSharingData(data)
		if self.MDList:
			print self.name, self.stockCode, data["stockCode"], data["close"], self.MDList[-1]["stockCode"]
	#逐笔成交触发函数
	def onRtnTradeSettlement(self, data):
		pass
	#买一队列触发函数
	def onRtnOrderQueue(self, data):
		pass
	#自动保存缓存触发函数
	def autosaveCache(self):
		#self.saveCache(data = self.data)
		self.saveCache(
			stockCodengDataList = self.timeSharingDataList)
	#------------------------------
	#策略实现函数
	#------------------------------
	def getTimeSharingData(self, data):
		if not self.timeSharingDataList:
			self.timeSharingDataList.append((copy.copy(data["dateTime"]), copy.copy(data["close"])))
		else:
			if data["dateTime"].minute != self.timeSharingDataList[-1][0].minute:
				self.timeSharingDataList.append((copy.copy(data["dateTime"]), copy.copy(data["close"])))
		if len(self.timeSharingDataList) > 100:
			del self.timeSharingDataList[0]