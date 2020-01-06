# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
from PyQt5.QtWidgets import QMainWindow, QApplication
from Ui_Ui_interface import Ui_MainWindow

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
        self.setWindowTitle("牵引供电系统计算软件")
        self.actionAT.triggered.connect(self.set_para)
    
    #添加AT牵引供电系统，上下行14根导线参数设置槽函数
    
    def set_para(self):
        from set_window import Dialog
        d = Dialog()
        d.exec_()
        
        
        
        



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()  
