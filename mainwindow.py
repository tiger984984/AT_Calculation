# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys
import sqlite3
from sqlite3 import connect
import os.path
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_mainwindow import Ui_MainWindow
from sql_setstructure_2 import sql_set
from show_results import results
from calculation_setting import set_cal
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
        self.actionpeizhi.triggered.connect(self.calculation_setting)#点击菜单栏计算参数配置-配置
        self.actionshuchu.triggered.connect(self.show_results)#点击菜单栏计算参数配置-配置
        
        
    def btn_open(self):#打开，获得所选文件地址
        self.fileName, _ = QFileDialog.getOpenFileName(self,"打开", "./user","数据库(*.db)")
        print(self.fileName)
        con = connect(self.fileName)
        cursor = con.cursor()
        select_mode = cursor.execute('select mode from base')
        self.mode = select_mode.fetchone()[0]
        print(self.mode)

    def btn_new(self):#点击“新建”蹦出新建界面
        self.Dialog_new = QDialog()
        self.Dialog_new.resize(400, 300)
        self.Dialog_new.setSizeGripEnabled(False)
        self.label_name = QtWidgets.QLabel(self.Dialog_new)
        self.label_name.setGeometry(QtCore.QRect(20, 70, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label")
        self.lineEdit_new = QtWidgets.QLineEdit(self.Dialog_new)
        self.lineEdit_new.setGeometry(QtCore.QRect(180, 70, 171, 25))
        self.lineEdit_new.setObjectName("lineEdit_new")
        self.pushButton = QtWidgets.QPushButton(self.Dialog_new)
        self.pushButton.setGeometry(QtCore.QRect(40, 230, 112, 34))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.Dialog_new)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 230, 112, 34))
        self.pushButton_2.setObjectName("pushButton_2")
        self.radioButton = QtWidgets.QRadioButton(self.Dialog_new)
        self.radioButton.setGeometry(QtCore.QRect(180, 120, 132, 22))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.Dialog_new)
        self.radioButton_2.setGeometry(QtCore.QRect(180, 160, 132, 22))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_chose = QtWidgets.QLabel(self.Dialog_new)
        self.label_chose.setGeometry(QtCore.QRect(20, 120, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label_chose.setFont(font)
        self.label_chose.setObjectName("label_2")

        self.retranslateUi(self.Dialog_new)
        self.pushButton_2.clicked.connect(self.Dialog_new.close)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog_new)
        
        _translate = QtCore.QCoreApplication.translate
        self.Dialog_new.setWindowTitle(_translate("Dialog_new", "新建"))
        self.label_name.setText(_translate("Dialog_new", "线路名称"))
        self.lineEdit_new.setText(_translate("Dialog_new", "请输入新建线路名称"))
        self.pushButton.setText(_translate("Dialog_new", "确定"))
        self.pushButton_2.setText(_translate("Dialog_new", "取消"))
        self.radioButton.setText(_translate("Dialog_new", "AT供电"))
        self.radioButton_2.setText(_translate("Dialog_new", "直接供电"))
        self.label_chose.setText(_translate("Dialog_new", "供电方式"))
        self.radioButton.setChecked(True)#默认选中AT供电方式
        
        self.pushButton_2.clicked.connect(self.Dialog_new.close)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog_new)#点击“取消”关闭
        self.pushButton.clicked.connect(self.new)#点击“确定”新建文件夹，复制缺省数据库
        self.retranslateUi(self.Dialog_new)
        self.Dialog_new.exec_()#模式对话框，不结束则置顶
        
       # self.pushButton.clicked.connect(self.new)#点击“确定”新建文件夹，复制缺省数据库
    def new(self):
        #新建的操作（文件夹＋数据库复制）
        #当前路径：程序所在路径（与user并列的路径）
        
        getname = self.lineEdit_new.text()#获取新建线路名称
        self.name = './user/'+getname#新建线路文件夹存储地址为./user/新建文件夹名称
        import os
        folder = os.path.exists(self.name)#判断是否存在将要新建的文件夹
        if not folder:
#            os.makedirs(self.name)#建立./user/新建文件夹
#            new_db = self.name+'/topology.db'#新建文件夹内的缺省db文件：./user/新建文件夹/topology.db
#            copyfile('./user/topology_test.db', new_db)#topology.db是由初始缺省文件topology_test复制的
#            self.fileName = './'+getname+'/topology.db'#获取数据库地址，传入show_setstructure,在class sql_set中作为filename传递。使用路径为./user，故fileName应为./新建文件夹/topology.db
#            self.Dialog_new.accept()#关闭“新建”对话框
#            self.show_setstructure()

            os.makedirs(self.name)
            new_db = self.name+'/'+getname+'topology.db'#新建文件夹内的缺省db文件：./user/新建文件夹/名字+topology.db
            if self.radioButton.isChecked()==True:
                self.mode = 'AT供电方式'
                #copyfile('./user/topology_test.db', new_db)
                copyfile('./data/ATtopology.db', new_db)
                self.fileName = './'+getname+'/'+getname+'topology.db'
            elif self.radioButton_2.isChecked()== True:
                self.mode = 'DT供电方式'
                copyfile('./data/TRtopology.db', new_db)
                self.fileName = './'+getname+'/'+getname+'topology.db'
                
            self.Dialog_new.accept()#关闭“新建”对话框
            self.show_setstructure()
        
        else:
            QMessageBox.information(self, '提示', '文件已存在！', QMessageBox.Close)
            self.Dialog_new.raise_()#让dialog保持在第一层
            self.lineEdit_new.setFocus()
#      
        
        
        
    def show_setstructure(self):
        print(self.fileName)
        #fileName=self.fileName
        #print(fileName)
        s=sql_set(self.fileName, self.mode)
        s.show()
        q = QtCore.QEventLoop()
        q.exec_()
    
    def show_results(self):
        print(self.fileName)
        s=results(self.fileName)
        s.show()
        q = QtCore.QEventLoop()
        q.exec_()
    
    def calculation_setting(self):
        print(self.fileName)
        s=set_cal(self.fileName)
        s.show()
        q = QtCore.QEventLoop()
        q.exec_()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main = MainWindow()
    Main.show()
    sys.exit(app.exec_())
  
