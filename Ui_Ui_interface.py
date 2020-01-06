# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\320\Desktop\牵引供电系统计算软件\Ui_interface.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(965, 675)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget_1 = QtWidgets.QTableWidget(self.centralWidget)
        self.tableWidget_1.setObjectName("tableWidget_1")
        self.tableWidget_1.setColumnCount(0)
        self.tableWidget_1.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget_1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 965, 23))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        self.menu_4 = QtWidgets.QMenu(self.menuBar)
        self.menu_4.setObjectName("menu_4")
        MainWindow.setMenuBar(self.menuBar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action10 = QtWidgets.QAction(MainWindow)
        self.action10.setObjectName("action10")
        self.action14 = QtWidgets.QAction(MainWindow)
        self.action14.setObjectName("action14")
        self.action2_14 = QtWidgets.QAction(MainWindow)
        self.action2_14.setObjectName("action2_14")
        self.actionDakai = QtWidgets.QAction(MainWindow)
        self.actionDakai.setObjectName("actionDakai")
        self.actionBaocun = QtWidgets.QAction(MainWindow)
        self.actionBaocun.setObjectName("actionBaocun")
        self.actionLcunwei = QtWidgets.QAction(MainWindow)
        self.actionLcunwei.setObjectName("actionLcunwei")
        self.action14_1 = QtWidgets.QAction(MainWindow)
        self.action14_1.setObjectName("action14_1")
        self.action10_1 = QtWidgets.QAction(MainWindow)
        self.action10_1.setObjectName("action10_1")
        self.action6_1 = QtWidgets.QAction(MainWindow)
        self.action6_1.setObjectName("action6_1")
        self.action10_2 = QtWidgets.QAction(MainWindow)
        self.action10_2.setObjectName("action10_2")
        self.action6_2 = QtWidgets.QAction(MainWindow)
        self.action6_2.setObjectName("action6_2")
        self.actionAT = QtWidgets.QAction(MainWindow)
        self.actionAT.setObjectName("actionAT")
        self.actionZhG = QtWidgets.QAction(MainWindow)
        self.actionZhG.setObjectName("actionZhG")
        self.menu_2.addAction(self.actionAT)
        self.menu_2.addAction(self.actionZhG)
        self.menu_4.addAction(self.actionDakai)
        self.menu_4.addAction(self.actionBaocun)
        self.menu_4.addAction(self.actionLcunwei)
        self.menuBar.addAction(self.menu_4.menuAction())
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "导线参数管理"))
        self.menu_2.setTitle(_translate("MainWindow", "供电计算"))
        self.menu_4.setTitle(_translate("MainWindow", "文件"))
        self.action.setText(_translate("MainWindow", "6"))
        self.action10.setText(_translate("MainWindow", "10"))
        self.action14.setText(_translate("MainWindow", "输入参数"))
        self.action2_14.setText(_translate("MainWindow", "输入参数"))
        self.actionDakai.setText(_translate("MainWindow", "打开"))
        self.actionBaocun.setText(_translate("MainWindow", "保存"))
        self.actionLcunwei.setText(_translate("MainWindow", "另存为"))
        self.action14_1.setText(_translate("MainWindow", "14根导线模型"))
        self.action10_1.setText(_translate("MainWindow", "10根导线模型"))
        self.action6_1.setText(_translate("MainWindow", "6根导线模型"))
        self.action10_2.setText(_translate("MainWindow", "10根导线模型"))
        self.action6_2.setText(_translate("MainWindow", "6根导线模型"))
        self.actionAT.setText(_translate("MainWindow", "AT供电方式"))
        self.actionZhG.setText(_translate("MainWindow", "直供方式"))
        
        
    def initUI(self): #定义初始化界面的方法
        self.resize(200,200)
        self.setWindowTitle('Example')
        self.move(200,200)
        self.setWindowIcon(QIcon('1.png')) #设置窗体标题图标
        self.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

