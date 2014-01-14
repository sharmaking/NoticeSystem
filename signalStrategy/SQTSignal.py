#!/usr/bin/python
# -*- coding: utf-8 -*-
#SQTSignal.py
import baseSignal
import copy
import datetime

class CSQTSignal(baseSignal.CBaseSignal):
	#------------------------------
	#继承重载函数
	#------------------------------
	#自定义初始化函数
	def customInit(self):
		self.name = "SQTSignal"
		self.timeSharingDataList = []	#分时时间数据
		self.highLowPointList = []		#高低点列表
		self.sectionLength = 60			#一小时分钟
		self.breakHighPointList = []	
		self.breakLowPointList	= []
		self.messageBox = []
	#行情数据触发函数
	def onRtnMarketData(self, data):
		if data["dateTime"].time() > datetime.time(9,30,0):
			self.getTimeSharingData(data)
			self.getBreakMessage(data)
	#逐笔成交触发函数
	def onRtnTradeSettlement(self, data):
		pass
	#买一队列触发函数
	def onRtnOrderQueue(self, data):
		pass
	#自动保存缓存触发函数
	def autosaveCache(self):
		self.saveCache(
			highLowPointList	= self.highLowPointList,
			timeSharingDataList	= self.timeSharingDataList)
	#------------------------------
	#策略实现函数
	#------------------------------
	#计算分时数据
	def getTimeSharingData(self, data):
		if not self.timeSharingDataList:
			self.timeSharingDataList.append((copy.copy(data["dateTime"]), copy.copy(data["close"])))
		else:
			if data["dateTime"].minute != self.timeSharingDataList[-1][0].minute and self.MDList:
				timeSharingData = copy.copy(data)
				timeSharingData["close"] = self.MDList[-1]["close"]
				self.getHighLowPoint(timeSharingData)
				self.timeSharingDataList.append((copy.copy(data["dateTime"]), copy.copy(timeSharingData["close"])))
		if len(self.timeSharingDataList) > 500:
			del self.timeSharingDataList[0]
	#计算分数高低点
	def getHighLowPoint(self, data):
		if len(self.timeSharingDataList) < self.sectionLength:
			copyTimeSharingData = copy.copy(self.timeSharingDataList)
		else:
			copyTimeSharingData = copy.copy(self.timeSharingDataList[len(self.timeSharingDataList)-self.sectionLength:])
		gtNum = 0
		ltNum = 0
		for timeSharingData in copyTimeSharingData:
			if data["close"] > timeSharingData[1]:
				gtNum = gtNum + 1
			if data["close"] < timeSharingData[1]:
				ltNum = ltNum + 1
		#高点
		if gtNum == self.sectionLength or gtNum == len(self.timeSharingDataList):
			if self.highLowPointList:
				if self.highLowPointList[-1][2] == "high":
					self.highLowPointList[-1] = (
						copy.copy(data["dateTime"]),
						copy.copy(data["close"]),
						"high")
				else:
					self.highLowPointList.append((
						copy.copy(data["dateTime"]),
						copy.copy(data["close"]),
						"high"))
			else:
				self.highLowPointList.append((
					copy.copy(data["dateTime"]),
					copy.copy(data["close"]),
					"high"))
		#低点
		if ltNum == self.sectionLength or ltNum == len(self.timeSharingDataList):
			if self.highLowPointList:
				if self.highLowPointList[-1][2] == "low":
					self.highLowPointList[-1] = (
						copy.copy(data["dateTime"]),
						copy.copy(data["close"]),
						"low")
				else:
					self.highLowPointList.append((
						copy.copy(data["dateTime"]),
						copy.copy(data["close"]),
						"low"))
			else:
				self.highLowPointList.append((
					copy.copy(data["dateTime"]),
					copy.copy(data["close"]),
					"low"))
	#计算突破分时高低点信号
	def getBreakMessage(self, data):
		breakHighPointList, breakLowPointList = self.isBreakHighLowPoint(data)
		for point in breakHighPointList:
			if not point in self.breakHighPointList:
				self.showMessage(True, point, data)
				self.breakHighPointList.append(point)
		for point in breakLowPointList:
			if not point in self.breakLowPointList:
				self.showMessage(False, point, data)
				self.breakLowPointList.append(point)
	def isBreakHighLowPoint(self, data):
		num = 0
		breakHighPointList = []
		breakLowPointList = []
		for point in self.highLowPointList[::-1]:
			if num > 1:
				if point[2] == "high":	#高点
					if data["close"] > point[1]:
						breakHighPointList.append(copy.copy(point))
				else:					#低点
					if data["close"] < point[1]:
						breakLowPointList.append(copy.copy(point))
			num = num +1
			if num > 5:
				break
		return breakHighPointList, breakLowPointList
	def showMessage(self, ishigh, point, data):
		message = {}
		if ishigh:
			message["type"] = "BreakHigh"
		else:
			message["type"] = "BreakLow"
		message["stockCode"]		= data["stockCode"]
		message["beBreakedPoint"]	= point
		message["breakTime"]		= data["dateTime"]
		message["breakPrice"]		= data["close"]
		self.messageBox.append(message)