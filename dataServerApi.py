#!/usr/bin/python
# -*- coding: utf-8 -*-
#dataServerApi.py
from DataApi_32 import CDataApi
import datetime

class CDataServerApi(CDataApi):
	#初始化接口
	def init(self, controller):
		self.controller = controller
		self.preDateTime = 0
		self.mainIF = ""
		self.initMainIFSubStock()
	#数据接收接口
	def onRtnDepthMarketData(self, dataType, data):
		self.controller.bufferStack[data["stockCode"][:6]].append((dataType,data))
		if self.controller.bufferStack.has_key("Multiple"):
			if dataType == 3 or dataType == 4 or dataType == 5:
				self.controller.bufferStack["Multiple"].append((dataType,data))
		if data["stockCode"][:6] == self.mainIF:
			if self.controller.bufferStack.has_key("IF0000"):
				self.controller.bufferStack["IF0000"].append((dataType,data))
		if dataType == 4:
			self.getMainIF(data["dateTime"])
	#数据传输结束
	def onRtnDataEnd(self):
		print "DataEnd"
	#------------------------
	#主力合约相关实现
	#------------------------
	#获取当然主力合约
	def getMainIF(self, dateTime):
		if not self.preDateTime:
			self.preDateTime = dateTime
		if dateTime.date() != self.preDateTime.date():
			self.calculateMainIF(dateTime)
		self.preDateTime = dateTime
	#计算主力合约
	def calculateMainIF(self, nowTime):
		if "IF0000" in self.controller.subStocks:
			mainIF = "IF"
			firstDayInThisMonth = nowTime.replace(day = 1)
			if nowTime.isocalendar()[1] - firstDayInThisMonth.isocalendar()[1] < 2 and nowTime.isocalendar()[2] < 5:
				mainIF = mainIF + nowTime.strftime("%y%m")
			else:
				mainIF = mainIF + nowTime.replace(month = (nowTime.month+1)).strftime("%y%m")
			self.mainIF = mainIF
			self.controller.subStocks.append(mainIF)
			self.controller.creatListener()
	#更新订阅合约
	def initMainIFSubStock(self):
		if self.controller.REQUEST_TYPE:
			nowTime = datetime.datetime.strptime(self.controller.START_TIME,"%Y-%m-%d %H:%M:%S")
		else:
			nowTime = datetime.datetime.now()
		self.calculateMainIF(nowTime)

