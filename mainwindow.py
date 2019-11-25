# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys
import sqlite3
import os.path
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_mainwindow import Ui_MainWindow
from sql_setstructure_2 import sql_set
from shutil import copyfile
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
        self.setupUi(self)
        self.initUi()
        
    def initUi(self):
        self.actionSetlines.triggered.connect(self.show_setstructure)#点击菜单栏结构配置
        self.actionOpen.triggered.connect(self.btn_open)#点击菜单栏打开
        self.actionNew.triggered.connect(self.btn_new)#点击菜单栏新建
#        
    def btn_open(self):#打开，获得所选文件地址
        self.fileName, _ = QFileDialog.getOpenFileName(self,"打开", "./user","数据库(*.db)")
        print(self.fileName)
        #self.fileName = fileName
        
    def btn_new(self):#点击“新建”蹦出新建界面
        self.Dialog_new = QDialog()
        #Dialog_new.setObjectName("Dialog_new")
        self.Dialog_new.resize(400, 300)
        self.Dialog_new.setSizeGripEnabled(False)
        self.label = QtWidgets.QLabel(self.Dialog_new)
        self.label.setGeometry(QtCore.QRect(30, 110, 101, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit_new = QtWidgets.QLineEdit(self.Dialog_new)
        self.lineEdit_new.setGeometry(QtCore.QRect(150, 110, 161, 25))
        self.lineEdit_new.setObjectName("lineEdit_new")
        self.pushButton = QtWidgets.QPushButton(self.Dialog_new)
        self.pushButton.setGeometry(QtCore.QRect(40, 230, 112, 34))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.Dialog_new)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 230, 112, 34))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(self.Dialog_new)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog_new)
        
        _translate = QtCore.QCoreApplication.translate
        self.Dialog_new.setWindowTitle(_translate("Dialog_new", "新建"))
        self.label.setText(_translate("Dialog_new", "线路名称"))
        self.lineEdit_new.setText(_translate("Dialog_new", "请输入新建线路名称"))
        self.pushButton.setText(_translate("Dialog_new", "确定"))
        self.pushButton_2.setText(_translate("Dialog_new", "取消"))
        self.pushButton_2.clicked.connect(self.Dialog_new.close)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog_new)#点击“取消”关闭
        self.pushButton.clicked.connect(self.new)#点击“确定”新建文件夹，复制缺省数据库
        self.retranslateUi(self.Dialog_new)
        #self.Dialog_new.show()
        self.Dialog_new.exec_()
        
       # self.pushButton.clicked.connect(self.new)#点击“确定”新建文件夹，复制缺省数据库
    def new(self):
        #新建的操作（文件夹＋数据库复制）
        #当前路径：程序所在路径（与user并列的路径）
        
        getname = self.lineEdit_new.text()#获取新建线路名称
        self.name = './user/'+getname#新建线路文件夹存储地址为./user/新建文件夹名称
        import os
        folder = os.path.exists(self.name)#判断是否存在将要存在的文件夹
        if not folder:
            #self.Dialog_new.close
            os.makedirs(self.name)#建立./user/新建文件夹
            #print(os.getcwd())
            new_db = self.name+'/topology.db'#新建文件夹内的缺省db文件：./user/新建文件夹/topology.db
            copyfile('./user/topology_test.db', new_db)#topology.db是由初始缺省文件topology_test复制的
            self.fileName = './'+getname+'/topology.db'#获取数据库地址，传入show_setstructure,在class sql_set中作为filename传递。使用路径为./user，故fileName应为./新建文件夹/topology.db
            self.Dialog_new.accept()
            self.show_setstructure()
            #self.Dialog_new.close
        else:
            QMessageBox.information(self, '提示', '文件已存在！', QMessageBox.Close)
            self.Dialog_new.raise_()#让dialog保持在第一层
            self.lineEdit_new.setFocus()
#        
        
        
        
    def show_setstructure(self):
        print(self.fileName)
        fileName=self.fileName
        #print(fileName)
        s=sql_set(fileName)
        s.show()
        q = QtCore.QEventLoop()
        q.exec_()
   
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main = MainWindow()
    Main.show()
    sys.exit(app.exec_())
  
