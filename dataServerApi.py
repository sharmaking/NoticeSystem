#!/usr/bin/python
# -*- coding: utf-8 -*-
#dataServerApi.py
from DataApi_32 import CDataApi

class CDataServerApi(CDataApi):
	#初始化接口
	def init(self, controller):
		self.controller = controller
		self.preDateTime = 0
		self.mainIF = ""
		#数据堆栈
		self.syncBufferStack = {} 	#缓存
	#数据接收接口
	def onRtnDepthMarketData(self, dataType, data):
		self.controller.bufferStack[data["stockCode"][:6]].append((dataType,data))
		if self.controller.bufferStack.has_key("Multiple"):
			if dataType == 3 or dataType == 4 or dataType == 5:
				self.controller.bufferStack["Multiple"].append((dataType,data))
		if data["stockCode"][:6] == self.mainIF:
			if self.controller.bufferStack.has_key("IF0000"):
				self.controller.bufferStack["IF0000"].append((dataType,data))
	#数据传输结束
	def onRtnDataEnd(self):
		print "DataEnd"
	#------------------------
	#同步数据相关事项
	#------------------------

	#------------------------
	#主力合约相关实现
	#------------------------
	#获取当然主力合约
	def getMainIF(self, mainIF):
		self.mainIF = mainIF
	#计算主力合约
	def calculateMainIF(nowTime):
		mainIF = "IF"
		firstDayInThisMonth = nowTime.replace(day = 1)
		if nowTime.isocalendar()[1] - firstDayInThisMonth.isocalendar()[1] < 2 and nowTime.isocalendar()[2] < 5:
			mainIF = mainIF + nowTime.strftime("%y%m")
		else:
			mainIF = mainIF + nowTime.replace(month = (nowTime.month+1)).strftime("%y%m")
		self.mainIF = mainIF

