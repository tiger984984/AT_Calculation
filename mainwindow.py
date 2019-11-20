# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_mainwindow import Ui_MainWindow

#from sql_setstructure_2 import sql_set

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
       # self.fileName=None
        self.setupUi(self)
        #self.menu_2.triggered[QtWidgets.QAction].connect(self.show_setstructure)
        self.actionSetlines.triggered.connect(self.show_setstructure)#点击菜单栏结构配置
        
        self.actionOpen.triggered.connect(self.btn_open)#点击菜单栏打开
       #self.wgt =QtWidgets.QWidget()
        #self.getAdd()
    def btn_open(self):
        fileName, _ = QFileDialog.getOpenFileName(self,"打开", "./user","All Files (*);;数据库 (*.db)")
        #if fileName:
        #self.fileName = fileName
        self.getAdd(fileName)
        return fileName
    def getAdd(self, fileName):
        #print(self.fileName)
        self.fileName=fileName
        #return self.fileName
    
    def show_setstructure(self):
     
        from sql_setstructure_2 import sql_set
       
        s=sql_set()
        s.show()
        q = QtCore.QEventLoop()
        q.exec_()
   
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main = MainWindow()
    #MainWindow.add = 10
    #print(MainWindow.add)
    Main.show()
    #print('---------')
   # print(Main.getAdd(fileName))
    sys.exit(app.exec_())
    #QCoreApplication.quit()
   
