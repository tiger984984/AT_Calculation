#from PyQt5 import QtGui, QtSvg
#from PyQt5.QtCore import pyqtSlot
#from PyQt5.QtWidgets import *
#from PyQt5 import QtCore,QtWidgets
#from Ui_sql_setstructure import Ui_Form
#import sqlite3
#from sqlite3 import connect
#from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
#import sys
#from PyQt5.QtCore import Qt
#from diyDelegate import TableDelegate
#from PyQt5.QtGui import QDoubleValidator
#from PyQt5.QtWebKitWidgets import QGraphicsWebView
#if __name__ == "__main__": 
#    app = QApplication(sys.argv) 
#
#    scene = QGraphicsScene() 
#    view = QGraphicsView(scene) 
#
#   # br = QtSvg.QGraphicsSvgItem("D:\Documents\eric6Document\test.svg").boundingRect() 
#
#    webview = QGraphicsWebView() 
#    webview.load(QtCore.QUrl("D:\Documents\eric6Document\test.py")) 
##    webview.setFlags(QGraphicsItem.ItemClipsToShape) 
##    webview.setCacheMode(QGraphicsItem.NoCache) 
##    webview.resize(br.width(), br.height()) 
#
#    scene.addItem(webview) 
##    view.resize(br.width()+10, br.height()+10) 
#    view.show() 
#    sys.exit(app.exec_()) 


from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(622, 545)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("D:\Documents\eric6Document\picture1.svg"))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "微信公众号：学点编程吧--svg图片显示"))
import svg_rc
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
