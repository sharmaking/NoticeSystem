#!/usr/bin/python
# -*- coding: utf-8 -*-
# mainWindow.py
import sys
from PyQt4 import QtGui, QtCore, uic
import copy
import datetime

class QMainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(QMainWindow,self).__init__()
		self.initUI()
		self.mainIF = "IF"
		self.preShowedMessageType = {
			"datetime"	: datetime.datetime.now(),
			"type"		: ""
		}

	#初始化窗口布局
	def initUI(self):
		uic.loadUi('ui/mainWindow.ui', self)
		self.setWindowTitle(u'信号客户端')
		self.statusBar().showMessage(u'正在连接服务器')	

	def showSocketLinkState(self, isSuccessful):
		if isSuccessful:
			self.statusBar().showMessage(u'链接成功!')
		else:
			self.statusBar().showMessage(u'服务器连接已断开！正在重连...')

	def showMessage(self, message):
		messageItem = QtGui.QListWidgetItem("%s  %s"%(message["breakTime"].strftime("%y-%m-%d %H:%M:%S"), message["breakPrice"]))
		messageKind = ""
		if message["type"] == "BreakHigh":
			messageQColor = QtGui.QColor("red")
			messageKind = u"高"
		else:
			messageQColor = QtGui.QColor("green")
			messageKind = u"低"
		messageBrush = QtGui.QBrush(messageQColor)
		messageItem.setForeground(messageBrush)
		messageItem.setWhatsThis(u"突破%s点: %s %s"%(messageKind, message["beBreakedPoint"][0].strftime("%y-%m-%d %H:%M:%S"), message["beBreakedPoint"][1]))

		messageItemII = QtGui.QListWidgetItem(u"突破%s点: %s %s"%(messageKind, message["beBreakedPoint"][0].strftime("%y-%m-%d %H:%M:%S"), message["beBreakedPoint"][1]))
		messageItemII.setForeground(messageBrush)
		
		if message["stockCode"] == "999999":
			self.Index_list.addItem(messageItem)
			self.Index_list.addItem(messageItemII)
		if message["stockCode"] == "IF0000":
			self.IF_list.addItem(messageItem)
			self.IF_list.addItem(messageItemII)

		self.saveShowedMessageType(message)

	def saveShowedMessageType(self, message):
		#判断信号类型
		messageType = ""
		if message["stockCode"] == "999999":
			messageType = "Index"
		if message["stockCode"] == "IF0000":
			messageType = "IF"
		#是合法信号
		if messageType:
			self.preShowedMessageType["datetime"] = datetime.datetime.now()
			self.preShowedMessageType["type"] = messageType
			#保存信号
			messageFile = open("messageFile.csv", "a")
			content = "%s %s %s; breakPoint: %s %s \n"%(message["stockCode"], message["breakTime"].strftime("%y-%m-%d %H:%M:%S"), message["breakPrice"], message["beBreakedPoint"][0].strftime("%y-%m-%d %H:%M:%S"), message["beBreakedPoint"][1])
			print "saveShowedMessageType", self.preShowedMessageType["datetime"]
			messageFile.write(content)
			messageFile.close()

	def clearMessage(self):
		if self.preShowedMessageType["type"]:
			if datetime.datetime.now() - self.preShowedMessageType["datetime"] > datetime.timedelta(minutes = 1):
				for x in xrange(len(self.Index_list)):
					self.Index_list.takeItem(x)
				for x in xrange(len(self.IF_list)):
					self.IF_list.takeItem(x)
				#---
				for x in xrange(len(self.Index_list)):
					self.Index_list.takeItem(x)
				for x in xrange(len(self.IF_list)):
					self.IF_list.takeItem(x)
				#self.Index_list.clear()
				#self.IF_list.clear()
				self.preShowedMessageType["type"] = ""
				print "clearMessage", datetime.datetime.now()

	def showMainIF(self, mainIF):
		if mainIF != self.mainIF:
			self.mainIF = mainIF
			self.MainIF_label.setText(mainIF)

	def closeEvent(self, event):
		r = QtGui.QMessageBox.question(self, u'退出', u'确定？', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No) 
		if r == QtGui.QMessageBox.Yes:
			event.accept()      # 退出 
		else: 
			event.ignore()      # 不退出

#信号监听器
class QListener(QtCore.QThread):
	def __init__(self, controller, Qmain):
		QtCore.QThread.__init__(self)
		self.controller = controller
		self.Qmain = Qmain
		self.connectState = False

	def __del__(self):
		self.wait()

	def run(self):
		while True:
			while self.controller.messageBox:
				self.Qmain.showMessage(copy.copy(self.controller.messageBox[0]))
				del self.controller.messageBox[0]
			self.Qmain.clearMessage()
			self.Qmain.showMainIF(self.controller.dataServerInstance.mainIF)
			self.showConnentState()
		self.terminate()

	def showConnentState(self):
		if self.controller.dataServerInstance.connectState != self.connectState:
			self.Qmain.showSocketLinkState(self.controller.dataServerInstance.connectState)
			self.connectState = self.controller.dataServerInstance.connectState


def main(controller):
	app = QtGui.QApplication(sys.argv)
	Qmain = QMainWindow()
	#创建信号监视进程
	messageListener = QListener(controller, Qmain)
	messageListener.start()
	#显示主窗口
	Qmain.show()
	sys.exit(app.exec_())
 	pass