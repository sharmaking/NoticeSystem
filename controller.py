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
#-----------------------
#定义全局变量
#-----------------------
#数据监听对象
g_listenerDict = {}		#每个合约一个个对象
#策略对象列表
g_strategyDict = {}		#key: 策略名，value：策略对象
#订阅股票列表
g_subStocks = []
#-----------------------
#注册策略
#-----------------------
#单只股票策略对象池
g_SSDict = {}
g_SSDict["baseSingal"] = signalStrategy.CBaseSingal()
g_SSDict["SQTSignal"] = signalStrategy.CSQTSignal()
#多只股票策略对象池
g_MSDict = {}
g_MSDict["baseMultiple"] = multipleStrategy.CBaseMultiple()
g_MSDict["SQTMultiple"] = multipleStrategy.CSQTMultiple()
#-----------------------
#实现函数
#-----------------------
#读取设置参数
execfile("config.ini")
#读取订阅股票
def loadSubStocks():
	global g_subStocks
	_fileReader  = open("./subStock.csv","r")
	while 1:
		line = _fileReader.readline()
		line = line.replace("\n","")
		if not line:
			break
		g_subStocks.append(line)
#创建数据连接对象
def creatDataServerLink():
	dataServerInstance = dataServerApi.CDataServerApi(HOST,PORT)
	dataServerInstance.init()
	dataServerInstance.connectServer()
	return dataServerInstance
#创建策略对象
def creatStrategyObject(needSignal, stock):
	strategyObjDict = {}
	if needSignal:	#单信号策略
		if not SUB_SIGNALS:		#如果没有订阅
			return False
		for signalName in SUB_SIGNALS:
			strategyObjDict[signalName] = copy.copy(g_SSDict[signalName])
			strategyObjDict[signalName].init(stock)
		return strategyObjDict
	else:			#多信号策略
		if not SUB_MULTIPLES:	#如果没有订阅
			return False
		for multipeName in SUB_MULTIPLES:
			strategyObjDict[multipeName] = copy.copy(g_MSDict[multipeName])
			strategyObjDict[multipeName].init("Multiple")
		return strategyObjDict
#创建监听对象
def creatListener(bufferStack):
	global g_listenerDict
	#单股票策略监听
	for stock in g_subStocks:
		if not g_listenerDict.has_key(stock):
			strategyObjDict = creatStrategyObject(True, stock)
			if strategyObjDict:
				bufferStack[stock]    = []
				newListener           = dataListener.CDataListener(stock, bufferStack[stock])
				newListener.getSignalStrategyObj(strategyObjDict)
				newListener.start()
				g_listenerDict[stock] = newListener
	#多股票策略监听
	strategyObjDict = creatStrategyObject(False,"Multiple")
	if strategyObjDict:
		bufferStack["Multiple"]		= []
		newListener					= dataListener.CDataListener("Multiple", bufferStack["Multiple"])
		newListener.getmultipleStrategyObj(strategyObjDict, g_listenerDict)
		newListener.start()
		g_listenerDict["Multiple"]	= newListener
#计算主力合约
def calculateMainIF():
	nowTime = datetime.datetime.now()
	mainIF = "IF"
	nowTime = datetime.datetime.now()
	firstDayInThisMonth = nowTime.replace(day = 1)
	if nowTime.isocalendar()[1] - firstDayInThisMonth.isocalendar()[1] < 2 and nowTime.isocalendar()[2] < 5:
		mainIF = mainIF + nowTime.strftime("%y%m")
	else:
		mainIF = mainIF + nowTime.replace(month = (nowTime.month+1)).strftime("%y%m")
	return mainIF
#更新订阅合约
def updateSubStock(socketLink, num):
	global g_subStocks
	if "IF0000" in g_subStocks:
		mainIF = calculateMainIF()
		g_subStocks.append(mainIF)
		socketLink.getMainIF(mainIF)
	while 1:
		nowTime = datetime.datetime.now()
		if nowTime.time() > datetime.time(9,14,0) and nowTime.time() < datetime.time(9,15,0):
			if "IF0000" in g_subStocks:
				mainIF = calculateMainIF()
				g_subStocks.append(mainIF)
				socketLink.getMainIF(mainIF)
			time.sleep(60)
#主入口
def main():
	#注册策略
	#载入订阅股票代码
	loadSubStocks()
	#创建数据连接对象
	dataServerInstance = creatDataServerLink()
	#注意监听更新订阅股票代码
	thread.start_new_thread(updateSubStock, (dataServerInstance,1))
	#创建数据监听器
	creatListener(dataServerInstance.bufferStack)
	#订阅股票代码
	dataServerInstance.subscibeStock(SUB_ALL_STOCK, g_subStocks)
	#请求数据
	dataServerInstance.requestData(
		REQUEST_TYPE,
		REQUEST_FLAG,
		datetime.datetime.strptime(START_TIME,"%Y-%m-%d %H:%M:%S"),
		datetime.datetime.strptime(END_TIME,"%Y-%m-%d %H:%M:%S"))
	