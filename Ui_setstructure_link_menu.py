# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Documents\eric6Document\setstructure_link_menu.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(938, 626)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_basic = QtWidgets.QWidget()
        self.tab_basic.setObjectName("tab_basic")
        self.tabWidget.addTab(self.tab_basic, "")
        self.tab_lines = QtWidgets.QWidget()
        self.tab_lines.setObjectName("tab_lines")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_lines)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget.addTab(self.tab_lines, "")
        self.tab_Telement = QtWidgets.QWidget()
        self.tab_Telement.setObjectName("tab_Telement")
        self.tabWidget.addTab(self.tab_Telement, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "结构配置"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_basic), _translate("Form", "基础"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_lines), _translate("Form", "纵向导线"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Telement), _translate("Form", "横向元件"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

