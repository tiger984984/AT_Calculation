
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QMenu
from PyQt5.QtGui import QIcon
import sys


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.statusBar().showMessage('准备就绪')
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('关注微信公众号：学点编程吧--子菜单')
        #三个菜单
        #菜单1：退出
        exitAct = QAction(QIcon('exit.png'), '退出(&E)', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('退出程序')
        exitAct.triggered.connect(qApp.quit)
        #菜单二：保存方式：子菜单：保存、另存为
        saveMenu = QMenu('保存方式(&S)', self)
        saveAct = QAction(QIcon('save.png'), '保存...', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('保存文件')
        saveasAct = QAction(QIcon('saveas.png'), '另存为...(&O)', self)
        saveasAct.setStatusTip('文件另存为')
        saveMenu.addAction(saveAct)#用addAction将保存添加到saveMenu（即保存方式）的子菜单中
        saveMenu.addAction(saveasAct)#同上添加另存为
        #菜单三：新建
        newAct = QAction(QIcon('new.png'), '新建(&N)', self)
        newAct.setShortcut('Ctrl+N')
        #创建菜单栏并加入菜单
        menubar = self.menuBar()#创建一个菜单栏
        fileMenu = menubar.addMenu('文件(&F)')
        fileMenu.addAction(newAct)
        fileMenu.addMenu(saveMenu)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAct)
        self.show()

    # #上下文菜单：右击鼠标：新建、保存、退出（可退出程序）
    # def contextMenuEvent(self, event):
    #    cmenu = QMenu(self)
    #    newAct = cmenu.addAction("新建")
    #    opnAct = cmenu.addAction("保存")
    #    quitAct = cmenu.addAction("退出")
    #    action = cmenu.exec_(self.mapToGlobal(event.pos()))#exec_()显示上下文菜单。并获取指针的坐标
    #    #mapToGlobal方法将窗口小部件坐标转换为全局屏幕坐标
    #    if action == quitAct:
    #        qApp.quit()
#创建工具栏
        toolbar = self.addToolBar('工具栏')
        toolbar.addAction(newAct)
        toolbar.addAction(exitAct)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

