#!/usr/bin/python
# -*- coding: utf-8 -*-
#controller.py
import copy
import time
import datetime
import thread
#自定义类
import dataServerApi
import dataListener
#载入策略
import signalStrategy
import multipleStrategy

class CController(object):
	def __init__(self):
		super(CController, self).__init__()
		#-----------------------
		#定义全局变量
		#-----------------------
		#数据监听对象
		self.listenerDict = {}		#每个合约一个个对象
		#策略对象列表
		self.strategyDict = {}		#key: 策略名，value：策略对象
		#订阅股票列表
		self.subStocks = []
		#数据缓存堆栈
		self.bufferStack = {}		#key: stockCode, value: list
		#信号槽
		self.messageBox = []
		#读取设置参数
		execfile("config.ini")
		#-----------------------
		self.run()
	#-----------------------
	#实现函数
	#-----------------------
	#读取订阅股票
	def loadSubStocks(self):
		_fileReader  = open("./subStock.csv","r")
		while 1:
			line = _fileReader.readline()
			line = line.replace("\n","")
			if not line:
				break
			self.subStocks.append(line)
	#创建数据连接对象
	def creatDataServerLink(self):
		self.dataServerInstance = dataServerApi.CDataServerApi(self.HOST,self.PORT)
		self.dataServerInstance.init(self)
		self.dataServerInstance.connectServer()
	#创建策略对象
	def creatStrategyObject(self, needSignal, stock):
		strategyObjDict = {}
		if needSignal:	#单信号策略
			if not self.SUB_SIGNALS:		#如果没有订阅
				return False
			for signalName in self.SUB_SIGNALS:
				singalObjStr = "signalStrategy.C%s%s()" %(signalName[0].upper(),signalName[1:])
				strategyObjDict[signalName] = eval(singalObjStr)
				strategyObjDict[signalName].init(stock, self)
			return strategyObjDict
		else:			#多信号策略
			if not self.SUB_MULTIPLES:	#如果没有订阅
				return False
			for multipeName in self.SUB_MULTIPLES:
				multipeObjStr = "multipleStrategy.C%s%s()" %(multipeName[0].upper(),multipeName[1:])
				strategyObjDict[multipeName] = eval(multipeObjStr)
				strategyObjDict[multipeName].init("Multiple", self)
			return strategyObjDict
	#创建监听对象
	def creatListener(self):
		#单股票策略监听
		for stock in self.subStocks:
			if not self.listenerDict.has_key(stock):
				strategyObjDict = self.creatStrategyObject(True, stock)
				if strategyObjDict:
					self.bufferStack[stock]		= []
					newListener           		= dataListener.CDataListener(stock, self.bufferStack)
					newListener.setDaemon(True)
					newListener.getSignalStrategyObj(strategyObjDict)
					newListener.start()
					self.listenerDict[stock]	= newListener
		#多股票策略监听
		if not self.listenerDict.has_key("Multiple"):
			strategyObjDict = self.creatStrategyObject(False,"Multiple")
			if strategyObjDict:
				self.bufferStack["Multiple"]	= []
				newListener						= dataListener.CDataListener("Multiple", self.bufferStack)
				newListener.setDaemon(True)
				newListener.getmultipleStrategyObj(strategyObjDict, self.listenerDict)
				newListener.start()
				self.listenerDict["Multiple"]	= newListener
		#订阅股票代码
		self.dataServerInstance.subscibeStock(self.SUB_ALL_STOCK, self.subStocks)
	#-----------------------
	#主入口
	#-----------------------
	def run(self):
		#载入订阅股票代码
		self.loadSubStocks()
		#创建数据连接对象
		self.creatDataServerLink()
		#创建数据监听器 and 订阅股票代码
		self.creatListener()
		#请求数据
		self.dataServerInstance.requestData(
			self.REQUEST_TYPE,
			self.REQUEST_FLAG,
			datetime.datetime.strptime(self.START_TIME,"%Y-%m-%d %H:%M:%S"),
			datetime.datetime.strptime(self.END_TIME,"%Y-%m-%d %H:%M:%S"))