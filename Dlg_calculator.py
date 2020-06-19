# -*- coding: utf-8 -*-

"""
Module implementing Dlg_calculator.
"""

#from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

from Ui_UI_calculator import Ui_Dialog#这个点不要
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Dlg_calculator(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    #定义几个公共变量
    
    lcdstring = ''
    #lcd上显示的字符，默认为空
    operation = ''
    #定义操作符
    currentNum = 0
    #当前数值
    previousNum = 0
    #之前的数值
    result = 0
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dlg_calculator, self).__init__(parent)
        self.setupUi(self)
        self.action()#定义本次需要的函数，信号与槽的关系
        
    def action(self):
        #定义按下数字执行的方法（信号与槽）
        self.connect(self.b0, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b1, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b2, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b3, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b4, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b5, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b6, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b7, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b8, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b9, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        self.connect(self.b_point, QtCore.SIGNAL('clicked()'), self.buttonClicked)
        #定义按下操作符执行的方法
        self.connect(self.b_pluse, QtCore.SIGNAL('clicked()'), self.opClicked)
        self.connect(self.b_sub, QtCore.SIGNAL('clicked()'), self.opClicked)
        self.connect(self.b_mul, QtCore.SIGNAL('clicked()'), self.opClicked)
        self.connect(self.b_div, QtCore.SIGNAL('clicked()'), self.opClicked)
        #定义按下清除键执行的方法
        self.connect(self.b_clear, QtCore.SIGNAL('clicked()'), self.clrClicked)
        #定义按下等于号执行的方法
        self.connect(self.b_equ, QtCore.SIGNAL('clicked()', self.eqClicked))
        
        #每一个槽对应的函数
    def buttonClicked(self):
        Dlg_calculator.lcdstring = Dlg_calculator.lcdstring + self.sender().text()#原本空值+text值
        self.lcd.display(Dlg_calculator.lcdstring)#显示
        Dlg_calculator.currentNum = float(Dlg_calculator.lcdstring)#强制转换，考虑小数点
    
    def opClicked(self):#按下操作符，首先把当前值currentNum赋给previousNum，
        Dlg_calculator.previousNum = Dlg_calculator.currentNum
        Dlg_calculator.currentNum = 0
        Dlg_calculator.lcdstring = ''
        Dlg_calculator.operation = self.sender().objectName()
    
    def clrClicked(self):
        Dlg_calculator.lcdstring = ''#lcd变量为空
        Dlg_calculator.operation = ''
        Dlg_calculator.currentNum = 0
        Dlg_calculator.previousNum = 0
        Dlg_calculator.result = 0 
        self.lcd.display(0)
        
    def eqClicked(self):
        if Dlg_calculator.operation == 'b_pluse':
            Dlg_calculator.result = Dlg_calculator.previousNum + Dlg_calculator.currentNum
            self.lcd.display(Dlg_calculator.result)
            
        if Dlg_calculator.operation == 'b_sub':
            Dlg_calculator.result = Dlg_calculator.previousNum - Dlg_calculator.currentNum
            self.lcd.display(Dlg_calculator.result)
            
        if Dlg_calculator.operation == 'b_mul':
            Dlg_calculator.result = Dlg_calculator.previousNum * Dlg_calculator.currentNum
            self.lcd.display(Dlg_calculator.result)
            
        if Dlg_calculator.operation == 'b_div':
            Dlg_calculator.result = Dlg_calculator.previousNum / Dlg_calculator.currentNum
            self.lcd.display(Dlg_calculator.result)
            
        Dlg_calculator.currentNum = Dlg_calculator
        Dlg_calculator.lcdstring = ''
            
            
    #主程序运行代码
    if __name__ == '__main__':
        app = QtWidgets.QApplication(sys.argv)
        mycal = Dlg_calculator()#生成我们自己建立的类的对象
        mycal.show()
        sys.exit(app.exec_())
