# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\软件New\topology.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(622, 574)
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        Dialog.setSizeGripEnabled(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBox1 = QtWidgets.QCheckBox(Dialog)
        self.checkBox1.setObjectName("checkBox1")
        self.verticalLayout_2.addWidget(self.checkBox1)
        self.checkBox2 = QtWidgets.QCheckBox(Dialog)
        self.checkBox2.setObjectName("checkBox2")
        self.verticalLayout_2.addWidget(self.checkBox2)
        self.checkBox3 = QtWidgets.QCheckBox(Dialog)
        self.checkBox3.setObjectName("checkBox3")
        self.verticalLayout_2.addWidget(self.checkBox3)
        self.checkBox4 = QtWidgets.QCheckBox(Dialog)
        self.checkBox4.setObjectName("checkBox4")
        self.verticalLayout_2.addWidget(self.checkBox4)
        self.checkBox5 = QtWidgets.QCheckBox(Dialog)
        self.checkBox5.setObjectName("checkBox5")
        self.verticalLayout_2.addWidget(self.checkBox5)
        self.checkBox6 = QtWidgets.QCheckBox(Dialog)
        self.checkBox6.setObjectName("checkBox6")
        self.verticalLayout_2.addWidget(self.checkBox6)
        self.checkBox7 = QtWidgets.QCheckBox(Dialog)
        self.checkBox7.setObjectName("checkBox7")
        self.verticalLayout_2.addWidget(self.checkBox7)
        self.checkBox8 = QtWidgets.QCheckBox(Dialog)
        self.checkBox8.setObjectName("checkBox8")
        self.verticalLayout_2.addWidget(self.checkBox8)
        self.checkBox9 = QtWidgets.QCheckBox(Dialog)
        self.checkBox9.setObjectName("checkBox9")
        self.verticalLayout_2.addWidget(self.checkBox9)
        self.checkBox10 = QtWidgets.QCheckBox(Dialog)
        self.checkBox10.setObjectName("checkBox10")
        self.verticalLayout_2.addWidget(self.checkBox10)
        self.checkBox11 = QtWidgets.QCheckBox(Dialog)
        self.checkBox11.setObjectName("checkBox11")
        self.verticalLayout_2.addWidget(self.checkBox11)
        self.checkBox12 = QtWidgets.QCheckBox(Dialog)
        self.checkBox12.setObjectName("checkBox12")
        self.verticalLayout_2.addWidget(self.checkBox12)
        self.checkBox13 = QtWidgets.QCheckBox(Dialog)
        self.checkBox13.setObjectName("checkBox13")
        self.verticalLayout_2.addWidget(self.checkBox13)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 1, 2, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.tableWidget.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkBox1.setText(_translate("Dialog", "导 线 选 型"))
        self.checkBox2.setText(_translate("Dialog", "AT 变 压 器"))
        self.checkBox3.setText(_translate("Dialog", "牵引变压器"))
        self.checkBox4.setText(_translate("Dialog", "上下行并联线"))
        self.checkBox5.setText(_translate("Dialog", "保护线pw1_钢轨ra1"))
        self.checkBox6.setText(_translate("Dialog", "综合地线e1_钢轨ra1"))
        self.checkBox7.setText(_translate("Dialog", "综合地线e1接地g"))
        self.checkBox8.setText(_translate("Dialog", "保护线pw2_钢轨ra3"))
        self.checkBox9.setText(_translate("Dialog", "综合地线e2_钢轨ra3"))
        self.checkBox10.setText(_translate("Dialog", "综合地线e2接地g"))
        self.checkBox11.setText(_translate("Dialog", "钢轨ra1_接地g"))
        self.checkBox12.setText(_translate("Dialog", "钢轨ra3_接地g"))
        self.checkBox13.setText(_translate("Dialog", "机  车"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

