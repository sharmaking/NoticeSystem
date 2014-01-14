#!/usr/bin/python
# -*- coding: utf-8 -*-
#dataListener.py
import threading

class CDataListener(threading.Thread):
	def __init__(self, name, bufferStack):
		super(CDataListener, self).__init__()
		self.stockCode = name
		self.name = "Thread-%s-Listener" %name
		self.bufferStack = bufferStack
		#策略对象
		self.type = True     		#监听类型： True 单股票策略监听，False 多股票策略监听
		self.signalObjDict = {}		#但股票策略对象列表
		self.listenerDict = {}
		self.multipleObjDict = {}
	#----------------------------
	#获得策略对象
	#----------------------------
	#单股票策略
	def getSignalStrategyObj(self, signalObjDict):
		self.signalObjDict.update(signalObjDict.items())
		self.type = True
	#多股票策略
	def getmultipleStrategyObj(self, multipleObjDict, listenerDict):
		self.multipleObjDict.update(multipleObjDict.items())
		self.listenerDict = listenerDict
		self.type = False
	#----------------------------
	#主函数，监听数据更新
	#----------------------------
	def run(self):
		while 1:
			while self.bufferStack[self.stockCode]:
				dataType, data = self.bufferStack[self.stockCode][0]
				del self.bufferStack[self.stockCode][0]
				self.dataListening(dataType, data)
	def dataListening(self, dataType, data):
		if self.type:
			for signalName, signalObj in self.signalObjDict.items():
				signalObj.dataListener(dataType, data)
		else:
			for multipleName, multipleObj in self.multipleObjDict.items():
				multipleObj.dataListener(dataType, data)
