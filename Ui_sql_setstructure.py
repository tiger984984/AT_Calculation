# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Documents\eric6Document\sql_setstructure.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1049, 746)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(30, 10, 971, 721))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 881, 172))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 60, 411, 35))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_2 = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_3.setFont(font)
        self.radioButton_3.setObjectName("radioButton_3")
        self.horizontalLayout.addWidget(self.radioButton_3)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 460, 881, 181))
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(60, 70, 442, 79))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 1, 2, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_4.setFont(font)
        self.radioButton_4.setObjectName("radioButton_4")
        self.gridLayout_3.addWidget(self.radioButton_4, 0, 0, 1, 1)
        self.comboBox_rou = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBox_rou.setEnabled(True)
        self.comboBox_rou.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBox_rou.setAcceptDrops(False)
        self.comboBox_rou.setToolTip("")
        self.comboBox_rou.setToolTipDuration(0)
        self.comboBox_rou.setEditable(True)
        self.comboBox_rou.setCurrentText("")
        self.comboBox_rou.setObjectName("comboBox_rou")
        self.gridLayout_3.addWidget(self.comboBox_rou, 0, 1, 1, 1)
        self.radioButton_5 = QtWidgets.QRadioButton(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_5.setFont(font)
        self.radioButton_5.setObjectName("radioButton_5")
        self.gridLayout_3.addWidget(self.radioButton_5, 1, 0, 1, 1)
        self.lineEdit_rou = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_rou.setEnabled(True)
        self.lineEdit_rou.setMinimumSize(QtCore.QSize(180, 0))
        self.lineEdit_rou.setAcceptDrops(False)
        self.lineEdit_rou.setToolTip("")
        self.lineEdit_rou.setObjectName("lineEdit_rou")
        self.gridLayout_3.addWidget(self.lineEdit_rou, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 2, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(100, 30, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_init = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_init.setGeometry(QtCore.QRect(210, 30, 61, 25))
        self.lineEdit_init.setObjectName("lineEdit_init")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(290, 30, 41, 21))
        self.label_7.setObjectName("label_7")
        self.lineEdit_end = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_end.setGeometry(QtCore.QRect(340, 30, 61, 25))
        self.lineEdit_end.setObjectName("lineEdit_end")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(420, 30, 16, 18))
        self.label_9.setObjectName("label_9")
        self.tableView_rou = QtWidgets.QTableView(self.groupBox_2)
        self.tableView_rou.setGeometry(QtCore.QRect(530, 10, 331, 141))
        self.tableView_rou.setObjectName("tableView_rou")
        self.pushButton_addrou = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_addrou.setGeometry(QtCore.QRect(470, 160, 31, 21))
        self.pushButton_addrou.setObjectName("pushButton_addrou")
        self.pushButton_delrou = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_delrou.setGeometry(QtCore.QRect(830, 160, 31, 21))
        self.pushButton_delrou.setObjectName("pushButton_delrou")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 240, 881, 172))
        self.groupBox_3.setObjectName("groupBox_3")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setGeometry(QtCore.QRect(60, 50, 141, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit_sectionlength = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_sectionlength.setGeometry(QtCore.QRect(220, 50, 200, 25))
        self.lineEdit_sectionlength.setObjectName("lineEdit_sectionlength")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(430, 50, 16, 18))
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(60, 110, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit_deltalength = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit_deltalength.setGeometry(QtCore.QRect(220, 110, 200, 25))
        self.lineEdit_deltalength.setObjectName("lineEdit_deltalength")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setGeometry(QtCore.QRect(430, 110, 16, 18))
        self.label_8.setObjectName("label_8")
        self.pushButton_save1 = QtWidgets.QPushButton(self.tab)
        self.pushButton_save1.setGeometry(QtCore.QRect(800, 640, 112, 34))
        self.pushButton_save1.setObjectName("pushButton_save1")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tableView = QtWidgets.QTableView(self.tab_2)
        self.tableView.setGeometry(QtCore.QRect(40, 30, 441, 601))
        self.tableView.setObjectName("tableView")
        self.pushButton_save2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_save2.setGeometry(QtCore.QRect(370, 640, 112, 34))
        self.pushButton_save2.setObjectName("pushButton_save2")
        self.pushButton_check = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_check.setGeometry(QtCore.QRect(0, 170, 31, 111))
        self.pushButton_check.setObjectName("pushButton_check")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.comboBox_rou.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "结构配置"))
        self.groupBox.setTitle(_translate("Form", "供电方式"))
        self.radioButton_2.setText(_translate("Form", "AT"))
        self.radioButton_3.setText(_translate("Form", "直供"))
        self.groupBox_2.setTitle(_translate("Form", "大地导电率"))
        self.label_6.setText(_translate("Form", "1/(Ω·cm)"))
        self.label_3.setText(_translate("Form", "1/(Ω·cm)"))
        self.radioButton_4.setText(_translate("Form", "土壤类型"))
        self.comboBox_rou.setStatusTip(_translate("Form", "选择地质情况"))
        self.comboBox_rou.setWhatsThis(_translate("Form", "选择地质情况"))
        self.radioButton_5.setText(_translate("Form", "自定义"))
        self.lineEdit_rou.setText(_translate("Form", "自定义导电率"))
        self.label_2.setText(_translate("Form", "区段"))
        self.label_7.setText(_translate("Form", "m  -"))
        self.label_9.setText(_translate("Form", "m"))
        self.pushButton_addrou.setText(_translate("Form", "+"))
        self.pushButton_delrou.setText(_translate("Form", "-"))
        self.groupBox_3.setTitle(_translate("Form", "供电臂"))
        self.label.setText(_translate("Form", "供电臂长度"))
        self.lineEdit_sectionlength.setText(_translate("Form", "请填写供电臂长度"))
        self.label_5.setText(_translate("Form", "m"))
        self.label_4.setText(_translate("Form", "基本分段长度"))
        self.lineEdit_deltalength.setText(_translate("Form", "请填写基本分段长度"))
        self.label_8.setText(_translate("Form", "m"))
        self.pushButton_save1.setText(_translate("Form", "保存"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "基础"))
        self.pushButton_save2.setText(_translate("Form", "保存"))
        self.pushButton_check.setText(_translate("Form", "查\n"
"看\n"
"参\n"
"数"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "导线选择"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "横向元件"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
