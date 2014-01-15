#!/usr/bin/python
# -*- coding: utf-8 -*-
import controller
import mainWindow

def main():
	mainController = controller.CController()
	#窗口显示
	mainWindow.main(mainController)
	pass

if __name__ == '__main__':
	main()