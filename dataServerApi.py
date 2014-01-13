#!/usr/bin/python
# -*- coding: utf-8 -*-
#dataServerApi.py
from DataApi_32 import CDataApi

class CDataServerApi(CDataApi):
	#初始化接口
	def init(self):
		self.mainIF = ""
		#数据堆栈
		self.bufferStack = {}	#每个合约一个堆栈
	#获取当然主力合约
	def getMainIF(self, mainIF):
		self.mainIF = mainIF
	#数据接收接口
	def onRtnDepthMarketData(self, dataType, data):
		self.bufferStack[data["stockCode"][:6]].append((dataType,data))
		if self.bufferStack.has_key("Multiple"):
			if dataType == 3 or dataType == 4 or dataType == 5:
				self.bufferStack["Multiple"].append((dataType,data))
		if data["stockCode"][:6] == self.mainIF:
			if self.bufferStack.has_key("IF0000"):
				self.bufferStack["IF0000"].append((dataType,data))
