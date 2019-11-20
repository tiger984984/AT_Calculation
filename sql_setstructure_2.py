"""
Module implementing sql_set.
"""
import sys
import os

from PyQt5 import QtGui, QtSvg
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtWidgets
from Ui_sql_setstructure import Ui_Form
from sqlite3 import connect
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtCore import Qt
from diyDelegate import TableDelegate
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWebKitWidgets import QGraphicsWebView
from mainwindow import MainWindow


class sql_set(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        #self.fileName = None
        super(sql_set, self).__init__(parent)
        self.setupUi(self)
        self.initUi()
        
    def initUi(self):
        #print('!!!!!!!!!!!!!!!!!!!!!!!')
        #Main = MainWindow()  
        #print(Main.fileName)
        rou=["干燥地区", "潮湿地区", "多岩地区", "平均情况"]
        self.comboBox_rou.addItems(rou)
        delegate = TableDelegate()#添加代理，添加下拉菜单（调用TableDelegate)
        self.tableView.setItemDelegate(delegate)#将代理（下拉菜单及数据）放入tableview
        
        #tab1中导电率单选框二选一有效
        self.radioButton_4.toggled.connect(lambda:self.on_radioButton_4_toggled(self.radioButton_4))
        self.radioButton_5.toggled.connect(lambda:self.on_radioButton_5_toggled(self.radioButton_5))
        
        #tab1中大地导电率点击+，数据库中添加一行分段情况
        self.pushButton_addrou.clicked.connect(self.addrou)
        self.pushButton_delrou.clicked.connect(self.delrou)
        
        #tab1中的保存按钮，按下后保存tab一中的内容到数据库base表
        self.pushButton_save1.clicked.connect(self.save1)
        
        self.linesModel()
        self.linesView()
        self.rou_ModelView()
        #tab2中的保存按钮，按下后保存tab2中的导线参数被保存至lines表的参数位置
        self.pushButton_save2.clicked.connect(self.save2)
        
        #self.pushButton.clicked.connect(self.check)
        self.pushButton_check.clicked.connect(self.check)
        
#        #显示svg
        self.svgWidget = QtSvg.QSvgWidget('D:/Documents/eric6Document/test.svg', self.tab_2)
        self.svgWidget.setGeometry(QtCore.QRect(500, 30, 471, 591))
       
        #self.widget.addItem(self.svgWidget)
        #self.svgWidget.setGeometry(50, 50, 755, 755)
        self.svgWidget.show()


        self.delrou()
        

    @pyqtSlot(bool)
    def on_radioButton_4_toggled(self, checked):
        self.lineEdit_rou.setEnabled(False)
        self.comboBox_rou.setEnabled(True)
    @pyqtSlot(bool)
    def on_radioButton_5_toggled(self, checked):
        self.lineEdit_rou.setEnabled(True)
        self.comboBox_rou.setEnabled(False)
        self.lineEdit_rou.setValidator(QDoubleValidator(self))#限制输入的内容
    
    def rou_ModelView(self):
        print('rou')        
        self.model_rou= QSqlTableModel(self.tableView_rou)#可以读和写的表格模型
        self.model_rou.setTable('rou')#设置要查询的表
        #self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)#设置函数编辑策略：手动提交，不自动提交
        self.model_rou.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_rou.select()#使用表的数据填充模型
        self.model_rou.setHeaderData(0, Qt.Horizontal, '导电率')
        self.model_rou.setHeaderData(1, Qt.Horizontal, '起始')
        self.model_rou.setHeaderData(2, Qt.Horizontal, '结束')
       # self.model_rou.setHorizontalHeaderLabels(['标题1','标题2','标题3','标题4'])
        self.model_rou.setFilter
        #self.selectionModel1 = self.tableView_rou.selectionModel()
        #self.selectionModel1.select(itemSelection, QtGui.QItemSelectionModel.Rows)#选取一行
        
        self.tableView_rou.setModel(self.model_rou)
        self.tableView_rou.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_rou.show()#显示tableView的内容
    
    def addrou(self):
        #获取大地导电率的数据，单选框，下拉菜单或自定义二选一
        rou_value=[0.001, 0.05, 0.00005, 0.0001]
        if self.radioButton_4.isChecked()==True:
            rou_index=self.comboBox_rou.currentIndex()#获得下拉菜单返回的索引
            rou=rou_value[rou_index]#根据索引获得相应数值
        else:
            rou = self.lineEdit_rou.text()
        print(rou)
        
        #获取起始点和结束点的位置
        initation_point = self.lineEdit_init.text()
        end_point = self.lineEdit_end.text()
        
        #新增一行并将数据添加进model
        rowNum =  self.model_rou.rowCount()
        self.model_rou.insertRow(rowNum)
        self.model_rou.setData(self.model_rou.index(rowNum, 0), rou)
        self.model_rou.setData(self.model_rou.index(rowNum, 1), initation_point)
        self.model_rou.setData(self.model_rou.index(rowNum, 2), end_point)
        
        self.model_rou.submitAll()
                
    def delrou(self):
        curRow = self.tableView_rou.currentIndex().row()
        self.model_rou.removeRow(curRow)
        self.model_rou.select()
        
        
    
    def save1(self):
        #保存基本环境参数内容到数据库
        #from mainwindow import MainWindow
        #os.chdir("../user")
        sqlname = 'topology_test.db'
       # sqlname = self.add
        #sqlname = dlg[0]
        #print(dlg[0])
        #sqlname = dlg[0]
        print(sqlname)
        con = connect(sqlname)
        cursor = con.cursor()
       
        #保存供电臂的数据到数据库
        section_length = self.lineEdit_sectionlength.text()
        delta_length = self.lineEdit_deltalength.text()
        cursor.execute('update base set section_length=?', (section_length, ))
        cursor.execute('update base set delta_length=?', (delta_length, ))
        
        con.commit()
        con.close()
        self.model_rou.submitAll()
        
    def linesModel(self):
        print('sql_setstructure')
       # print(MainWindow.add)
        #设置topogy数据库模型视图
        #os.path.dirname(__file__)
        #os.chdir('./user')
        os.chdir('D:/Documents/eric6Document/user')
        self.db = QSqlDatabase.addDatabase("QSQLITE")#设置数据库的数据库驱动类型
        self.db.setDatabaseName('topology_test.db')#设置连接的数据库
        
        self.model = QSqlTableModel(self.tableView)#可以读和写的表格模型
        self.model.setTable('lines')#设置要查询的表
        #self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)#设置函数编辑策略：手动提交，不自动提交
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()#使用表的数据填充模型
        self.model.setHeaderData(0, Qt.Horizontal, 'ID')
        self.model.setHeaderData(1, Qt.Horizontal, '导线名')
        self.model.setHeaderData(2, Qt.Horizontal, '型号')
        self.model.setHeaderData(3, Qt.Horizontal, '电阻')
        self.model.setHeaderData(4, Qt.Horizontal, '计算半径')
        self.model.setHeaderData(5, Qt.Horizontal, '等效半径')
        self.model.setHeaderData(6, Qt.Horizontal, '相对磁导率')
        self.model.setHeaderData(7, Qt.Horizontal, '导线电导率')
        self.model.setHeaderData(8, Qt.Horizontal, '位置(x轴)')
        self.model.setHeaderData(9, Qt.Horizontal, '位置(y轴)')
        self.model.setFilter
        
        #self.db.close()
        #QSqlDatabase.removeDatabase("QSQLITE")        
    
    def linesView(self):
      
        self.tableView.verticalHeader().hide()
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.tableView.setModel(self.model)#将Model（即数据库模型）放入tableView中
        self.tableView.show()#显示tableView的内容
        self.tableView.setColumnHidden(0, True)#隐藏ID列
        self.tableView.setColumnHidden(3, True)
        self.tableView.setColumnHidden(4, True)
        self.tableView.setColumnHidden(5, True)
        self.tableView.setColumnHidden(6, True)
        self.tableView.setColumnHidden(7, True)

    def save2(self):  
        os.chdir("../data")
        linesource = 'line_source.db'
        con1 = connect(linesource)
        cursor1 = con1.cursor()
        os.chdir('../user')
        con2 = connect('topology_test.db')
        cursor2 = con2.cursor()
        print('------------------------------------')
        for row in range(14):

            if row in [0, 1, 2, 5, 6, 7, 8, 9, 12, 13]:
                #record(model中的第几行），value（model中的取值），取出某行type_name列的值
                Type_name=self.model.record(row).value('type_name')
                print(Type_name)
                read=cursor1.execute('select resistance,radius,equvalent_radius,rho,mu_r from lines_source where type_name=?', (Type_name, ))
                allpara = list(read.fetchall())[0]
                print(allpara)
                n=row+1
                cursor2.execute('UPDATE lines SET resistance=?,radius=?,equivalent_radius=?,rho=?,mu_r=? where ID=?', (allpara[0],allpara[1],allpara[2], allpara[3],allpara[4], n))
                #self.model.setData(self.model.index(n, ) ,'value')
            else:
                Type_name=self.model.record(row).value('type_name')
                print(Type_name)
                read=cursor1.execute('select resistance,radius,equvalent_radius,rho,mu_r from rail_source where type_name=?', (Type_name, ))
                allpara = list(read.fetchall())[0]
                print(allpara)
                n=row+1
                cursor2.execute('UPDATE lines SET resistance=?,radius=?,equivalent_radius=?,rho=?,mu_r=? where ID=?', (allpara[0],allpara[1],allpara[2], allpara[3],allpara[4], n))
                
        con2.commit()
        con1.close()
        con2.close()
        
        
        
    def check(self):
        #self.linesModel()
        
        dlg = QDialog()        
        view2=QtWidgets.QTableView(dlg)
        self.model.select()#选择导线保存（save2)之后数据库更新，需要重新检索数据库调入model的数据中 ，否则界面无法显示更新的数据     
        view2.setModel(self.model)
        view2.verticalHeader().hide()
        view2.setColumnHidden(0, True)#隐藏ID列
        #view2.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置view2不可编辑（trigger无效）
        #view2.setEditTriggers(EditTriggers triggers)
        layout = QVBoxLayout()
        layout.addWidget(view2)
        dlg.setLayout(layout)
        dlg.resize(1400, 800)
        dlg.show()
        q = QtCore.QEventLoop()
        q.exec_()


#if __name__== "__main__":
#    app = QApplication(sys.argv)
#    Test = sql_set()
#    
#    
#    Test.show()
#    sys.exit(app.exec_())
#    
