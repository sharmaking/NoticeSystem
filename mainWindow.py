#!/usr/bin/python
# -*- coding: utf-8 -*-
# mainWindow.py
class QMainWindow(QtGui.QMainWindow):
	def __init__(self, connectSuccessful):
		super(QMainWindow,self).__init__()
		self.connectSuccessful = connectSuccessful
		self.initUI()

		self.initEventConnection()

	#初始化窗口布局
	def initUI(self):
		uic.loadUi('ui/mainWindow.ui', self)
		self.setWindowTitle(u'信号客户端')

		self.graphicsView = QtGui.QGraphicsView()
		self.setCentralWidget(self.graphicsView)

		#qss_file = open('style.css').read()
		#self.setStyleSheet(qss_file)
		if self.connectSuccessful:
			self.statusBar().showMessage('Connenct Successful!')
		else:
			self.statusBar().showMessage('Connenct Failure! Please Contact to Administrator!')

	#设置事件关联
	def initEventConnection(self):
		self.mainLayout = QtGui.QGraphicsLinearLayout()
		self.mainLayout.setOrientation(QtCore.Qt.Vertical)
		self.mainLayout.setSpacing(0)

		self.pixmap = signalItem.getSignalWidget()
		self._s = copy.copy(self.pixmap)

		mainWidget = QtGui.QGraphicsWidget()
		mainWidget.setLayout(self.mainLayout)

		scene = QtGui.QGraphicsScene()
		scene.addItem(mainWidget)
		self.graphicsView.setScene(scene)
		pass