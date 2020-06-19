#coding=utf-8
from PyQt5.QtWidgets import QApplication,QMainWindow
import sys
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()
    def InitUI(self):
        self.statusBar().showMessage('准备就绪')#第一个调用创建一个状态栏
        self.setGeometry(300,300,400,400)
        self.setWindowTitle('状态栏')
        self.show()

if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
