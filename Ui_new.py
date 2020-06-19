# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\牵引供电-朱明\new.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_new(object):
    def setupUi(self, Dialog_new):
        Dialog_new.setObjectName("Dialog_new")
        Dialog_new.resize(400, 300)
        Dialog_new.setSizeGripEnabled(False)
        self.label = QtWidgets.QLabel(Dialog_new)
        self.label.setGeometry(QtCore.QRect(20, 70, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit_new = QtWidgets.QLineEdit(Dialog_new)
        self.lineEdit_new.setGeometry(QtCore.QRect(180, 70, 171, 25))
        self.lineEdit_new.setObjectName("lineEdit_new")
        self.pushButton = QtWidgets.QPushButton(Dialog_new)
        self.pushButton.setGeometry(QtCore.QRect(40, 230, 112, 34))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog_new)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 230, 112, 34))
        self.pushButton_2.setObjectName("pushButton_2")
        self.radioButton = QtWidgets.QRadioButton(Dialog_new)
        self.radioButton.setGeometry(QtCore.QRect(180, 120, 132, 22))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog_new)
        self.radioButton_2.setGeometry(QtCore.QRect(180, 160, 132, 22))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_2 = QtWidgets.QLabel(Dialog_new)
        self.label_2.setGeometry(QtCore.QRect(20, 120, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog_new)
        self.pushButton_2.clicked.connect(Dialog_new.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog_new)

    def retranslateUi(self, Dialog_new):
        _translate = QtCore.QCoreApplication.translate
        Dialog_new.setWindowTitle(_translate("Dialog_new", "新建"))
        self.label.setText(_translate("Dialog_new", "线路名称"))
        self.lineEdit_new.setText(_translate("Dialog_new", "请输入新建线路名称"))
        self.pushButton.setText(_translate("Dialog_new", "确定"))
        self.pushButton_2.setText(_translate("Dialog_new", "取消"))
        self.radioButton.setText(_translate("Dialog_new", "AT供电"))
        self.radioButton_2.setText(_translate("Dialog_new", "直接供电"))
        self.label_2.setText(_translate("Dialog_new", "供电方式"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_new = QtWidgets.QDialog()
    ui = Ui_Dialog_new()
    ui.setupUi(Dialog_new)
    Dialog_new.show()
    sys.exit(app.exec_())

