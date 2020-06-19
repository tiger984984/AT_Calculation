"""
Module implementing sql_set.
"""
#-*- coding: UTF-8 -*-
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
#from mainwindow import MainWindow


class sql_set(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self,fileName, mode, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(sql_set, self).__init__(parent)
        self.fileName = fileName
        self.mode = mode
        self.setupUi(self)
        self.initUi()
        
    def initUi(self):
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
        
#        #显示导线选择tab2的svg
        self.PictureShow()
        #self.widget.addItem(self.svgWidget)
        #self.svgWidget.setGeometry(50, 50, 755, 755)
   #     self.svgWidget.show()
        
        self.setelement()

        self.delrou()
        
        self.treeWidget.clicked.connect(self.onClicked)
        
        #self.pushButton_add.clicked.connect(self.addAT)
   
            
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
        sqlname=self.fileName
        print(sqlname)
        con = connect(sqlname)
        cursor = con.cursor()
       
        #保存供电臂的数据到数据库
        Length = self.lineEdit_sectionlength.text()
        block_length = self.lineEdit_deltalength.text()
        cursor.execute('update base set Length=?', (Length, ))
        cursor.execute('update base set block_length=?', (block_length, ))
        
        con.commit()
        con.close()
        self.model_rou.submitAll()
        
        
    def linesModel(self):
        print('sql_setstructure')
        #设置topogy数据库模型视图
        #os.path.dirname(__file__)
        #os.chdir('./user')
        #os.chdir('D:/Documents/eric6Document/user')
        os.chdir('./user')
        self.db = QSqlDatabase.addDatabase("QSQLITE")#设置数据库的数据库驱动类型
        #self.db.setDatabaseName('topology_test.db')#设置连接的数据库
        self.db.setDatabaseName(self.fileName)
        self.model = QSqlTableModel(self.tableView)#可以读和写的表格模型
        self.model.setTable('lines')#设置要查询的表
        #self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)#设置函数编辑策略：手动提交，不自动提交
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.select()#使用表的数据填充模型
        self.model.setHeaderData(0, Qt.Horizontal, 'ID')
        self.model.setHeaderData(1, Qt.Horizontal, '导线名')
        self.model.setHeaderData(2, Qt.Horizontal, '型号')
        self.model.setHeaderData(3, Qt.Horizontal, '计算截面积(mm2)')
        self.model.setHeaderData(4, Qt.Horizontal, '单位质量(kg/km)')
        self.model.setHeaderData(5, Qt.Horizontal, '导电率(S/m)')
        self.model.setHeaderData(6, Qt.Horizontal, '持续载流量(A)')
        self.model.setHeaderData(7, Qt.Horizontal, '计算半径(mm)')
        self.model.setHeaderData(8, Qt.Horizontal, '等效半径(mm)')
        self.model.setHeaderData(9, Qt.Horizontal, '直流电阻(Ω)')
        self.model.setHeaderData(10, Qt.Horizontal, '直流电阻(Ω)')
        self.model.setHeaderData(11, Qt.Horizontal, '电阻率(Ω*m)-1')
        self.model.setHeaderData(12, Qt.Horizontal, '坐标x(mm)')
        self.model.setHeaderData(13, Qt.Horizontal, '坐标y(mm)')
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
        self.tableView.setColumnHidden(8, True)
        self.tableView.setColumnHidden(9, True)
        self.tableView.setColumnHidden(10, True)
        self.tableView.setColumnHidden(11, True)
        
    def PictureShow(self):  
        if self.mode == 'AT供电方式':
            self.svgWidget = QtSvg.QSvgWidget('../images/AT架设图.svg', self.tab_2)
        elif self.mode == 'DT供电方式':
            self.svgWidget = QtSvg.QSvgWidget('../images/TR架设图.svg', self.tab_2)
        self.svgWidget.setGeometry(QtCore.QRect(500, 30, 471, 591))
        self.svgWidget.show()

    def save2(self):  
        os.chdir("../data")
        #linesource = 'line_source.db'
        linesource = 'source_lines.db'
        con1 = connect(linesource)
        cursor1 = con1.cursor()
        os.chdir('../user')
        #con2 = connect('topology_test.db')
        con2 = connect(self.fileName)
        cursor2 = con2.cursor()
        print('------------------------------------')
        for row in range(14):

            if row in [0, 1, 2, 5, 6, 7, 8, 9, 12, 13]:
                #record(model中的第几行），value（model中的取值），取出某行type_name列的值
                #Type_name=self.model.record(row).value('type_name')
                Line_mode=self.model.record(row).value('line_mode')
                print(Line_mode)
                #read=cursor1.execute('select resistance,radius,equvalent_radius,rho,mu_r from lines_source where type_name=?', (Type_name, ))
                read=cursor1.execute('select line_area,line_unit_mass,line_conductivity,line_Current_density,line_Calculation_radius,\
                line_Equivalent_radius,line_Dc_resistance,line_Magnetic_permeability,line_Relative_permeability from lines where line_mode=?', (Line_mode, ))
                allpara = list(read.fetchall())[0]
                #allpara = list(read.fetchall())
                print('------------222222222333333333333')
                #print(read.fetchall())[0]
                n=row+1
                #cursor2.execute('UPDATE lines SET resistance=?,radius=?,equivalent_radius=?,rho=?,mu_r=? where ID=?', (allpara[0],allpara[1],allpara[2], allpara[3],allpara[4], n))
                cursor2.execute('UPDATE lines SET line_area=?,line_unit_mass=?,line_conductivity=?,line_Current_density=?,line_Calculation_radius=?,line_Equivalent_radius=?,line_Dc_resistance=?,line_Magnetic_permeability=?,line_Relative_permeability=? \
                where ID=?',(allpara[0],allpara[1],allpara[2], allpara[3],allpara[4],allpara[5], allpara[6],allpara[7],allpara[8],n))
                #self.model.setData(self.model.index(n, ) ,'value')
            else:
                Line_mode=self.model.record(row).value('Line_mode')
                print(Line_mode)
                read=cursor1.execute('select line_area,line_unit_mass,line_conductivity,line_Current_density,line_Calculation_radius,line_Equivalent_radius,line_Dc_resistance,line_Magnetic_permeability,line_Relative_permeability from rail where line_mode=?', (Line_mode, ))
                allpara = list(read.fetchall())[0]
                print(allpara)
                n=row+1
                cursor2.execute('UPDATE lines SET line_area=?,line_unit_mass=?,line_conductivity=?,line_Current_density=?,line_Calculation_radius=?,line_Equivalent_radius=?,line_Dc_resistance=?,line_Magnetic_permeability=?,line_Relative_permeability=? \
                where ID=?',(allpara[0],allpara[1],allpara[2], allpara[3],allpara[4],allpara[5], allpara[6],allpara[7],allpara[8],n))
                
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

    #对横向元件的选择配置界面进行初始设定
    def setelement(self):
        self.treeWidget.setColumnWidth(0, 250)#指定分类列的宽度
     
    def onClicked(self, qmodelLindex):
        item = self.treeWidget.currentItem()
        print(item.text(0))
        if item.text(0)=='自耦变压器':
            self.AT_ModelView()
        elif item.text(0)=='牵引变压器':
            self.TractionTransformer_ModelView()
        elif item.text(0)=='上下行并联线':
            self.UpDownConnection_ModelView()
        elif item.text(0)=='保护线pw1-钢轨ra1':
            self.Pw1Ra1_ModelView()
        elif item.text(0)=='综合地线e1-钢轨ra1':
            self.E1Ra1_ModelView()
        elif item.text(0)=='保护线pw2-钢轨ra3':
            self.Pw2Ra3_ModelView()
        elif item.text(0)=='综合地线e2-钢轨ra3':
            self.E2Ra3_ModelView()
        elif item.text(0)=='钢轨ra1-大地g':
            self.Ra1G_ModelView()
        elif item.text(0)=='钢轨ra3-大地g':
            self.Ra3G_ModelView()
        elif item.text(0)=='综合地线e1-大地g':
            self.E1G_ModelView()
        elif item.text(0)=='综合地线e2-大地g':
            self.E2G_ModelView()
        elif item.text(0)=='并联电阻':
            self.ParaR_ModelView()


    def AT_ModelView(self):
        self.model_AT = QSqlTableModel(self.tableView_element)
        self.model_AT.setTable('AT')#设置要查询的表
        self.model_AT.setEditStrategy(QSqlTableModel.OnFieldChange)#所有变更实时更新到数据库中
        self.model_AT.select()#使用表的数据填充模型
        self.model_AT.setHeaderData(0, Qt.Horizontal, 'AT名称')
        self.model_AT.setHeaderData(1, Qt.Horizontal, 'AT型号')
        self.model_AT.setHeaderData(2, Qt.Horizontal, '位置(km)')
        self.model_AT.setHeaderData(3, Qt.Horizontal, '漏导纳实部（Ω）')
        self.model_AT.setHeaderData(4, Qt.Horizontal, '漏导纳虚部（Ω）')
        self.model_AT.setFilter
        
        self.tableView_element.setModel(self.model_AT)
        self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#平均分布一整行
        
        self.tableView_element.show()#显示tableView的内容
        
        self.pushButton_add.clicked.connect(self.addAT)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delAT)#按减号删除一行
        #self.model_AT.select()
    def addAT(self):
        rowNum =  self.model_AT.rowCount()
        self.model_AT.insertRow(rowNum)
        #self.model_AT.select()
        self.model_AT.submitAll()
        #self.model_AT.select()
    def delAT(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_AT.removeRow(curRow)
        self.model_AT.select()
        
    def TractionTransformer_ModelView(self):
        self.model_TT = QSqlTableModel(self.tableView_element)
        self.model_TT.setTable('traction_transformer')#设置要查询的表
        self.model_TT.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_TT.select()#使用表的数据填充模型
        self.model_TT.setHeaderData(0, Qt.Horizontal, '牵引变压器名称')
        self.model_TT.setHeaderData(1, Qt.Horizontal, '型号')
        self.model_TT.setHeaderData(2, Qt.Horizontal, '位置(km)')
        self.model_TT.setHeaderData(3, Qt.Horizontal, '额定容量(MVA)')
        self.model_TT.setHeaderData(4, Qt.Horizontal, '变压比')
        self.model_TT.setHeaderData(5, Qt.Horizontal, '短路电压比')
        self.model_TT.setFilter
        
        self.tableView_element.setModel(self.model_TT)
        self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        
        self.pushButton_add.clicked.connect(self.addTT)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delTT)#按减号删除一行
    def addTT(self):
        rowNum =  self.model_TT.rowCount()
        self.model_TT.insertRow(rowNum)
        #self.model_AT.select()
        self.model_TT.submitAll()
        #self.model_AT.select()
    def delTT(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_TT.removeRow(curRow)
        self.model_TT.select()    
    
        
    def UpDownConnection_ModelView(self):
        self.model_UD = QSqlTableModel(self.tableView_element)
        self.model_UD.setTable('up_down_connection')#设置要查询的表
        self.model_UD.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_UD.select()#使用表的数据填充模型
        self.model_UD.setHeaderData(0, Qt.Horizontal, '位置(km)')
        self.model_UD.setFilter
        
        self.tableView_element.setModel(self.model_UD)
        #self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        
        self.pushButton_add.clicked.connect(self.addUD)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delUD)#按减号删除一行
    def addUD(self):
        rowNum =  self.model_UD.rowCount()
        self.model_UD.insertRow(rowNum)
        self.model_UD.submitAll()
    def delUD(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_UD.removeRow(curRow)
        self.model_UD.select()    
        
    def Pw1Ra1_ModelView(self):
        self.model_P1R1 = QSqlTableModel(self.tableView_element)
        self.model_P1R1.setTable('pw1_ra1')#设置要查询的表
        self.model_P1R1.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_P1R1.select()#使用表的数据填充模型
        self.model_P1R1.setHeaderData(0, Qt.Horizontal, '位置(km)')
        self.model_P1R1.setFilter
        
        self.tableView_element.setModel(self.model_P1R1)
        #self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        
        self.pushButton_add.clicked.connect(self.addP1R1)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delP1R1)#按减号删除一行
    def addP1R1(self):
        rowNum =  self.model_P1R1.rowCount()
        self.model_P1R1.insertRow(rowNum)
        self.model_P1R1.submitAll()
    def delP1R1(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_P1R1.removeRow(curRow)
        self.model_P1R1.select()    
        
    def E1Ra1_ModelView(self):
        self.model_E1R1 = QSqlTableModel(self.tableView_element)
        self.model_E1R1.setTable('e1_ra1')#设置要查询的表
        self.model_E1R1.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_E1R1.select()#使用表的数据填充模型
        self.model_E1R1.setHeaderData(0, Qt.Horizontal, '位置(km)')
        self.model_E1R1.setFilter
        
        self.tableView_element.setModel(self.model_E1R1)
        #self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        self.pushButton_add.clicked.connect(self.addE1R1)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delE1R1)#按减号删除一行
    def addE1R1(self):
        rowNum =  self.model_E1R1.rowCount()
        self.model_E1R1.insertRow(rowNum)
        self.model_E1R1.submitAll()
    def delE1R1(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_E1R1.removeRow(curRow)
        self.model_E1R1.select()  
        
    def Pw2Ra3_ModelView(self):
        self.model_P2R3 = QSqlTableModel(self.tableView_element)
        self.model_P2R3.setTable('pw2_ra3')#设置要查询的表
        self.model_P2R3.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_P2R3.select()#使用表的数据填充模型
        self.model_P2R3.setHeaderData(0, Qt.Horizontal, '位置(km)')
        self.model_P2R3.setFilter
        
        self.tableView_element.setModel(self.model_P2R3)
        #self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        self.pushButton_add.clicked.connect(self.addP2R3)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delP2R3)#按减号删除一行
    def addP2R3(self):
        rowNum =  self.model_P2R3.rowCount()
        self.model_P2R3.insertRow(rowNum)
        self.model_P2R3.submitAll()
    def delP2R3(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_P2R3.removeRow(curRow)
        self.model_P2R3.select()  
        
    def E2Ra3_ModelView(self):
        self.model_E2R3 = QSqlTableModel(self.tableView_element)
        self.model_E2R3.setTable('e2_ra3')#设置要查询的表
        self.model_E2R3.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_E2R3.select()#使用表的数据填充模型
        self.model_E2R3.setHeaderData(0, Qt.Horizontal, '位置(km)')
        self.model_E2R3.setFilter
        
        self.tableView_element.setModel(self.model_E2R3)
        #self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        self.pushButton_add.clicked.connect(self.addE2R3)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delE2R3)#按减号删除一行
    def addE2R3(self):
        rowNum =  self.model_E2R3.rowCount()
        self.model_E2R3.insertRow(rowNum)
        self.model_E2R3.submitAll()
    def delE2R3(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_E2R3.removeRow(curRow)
        self.model_E2R3.select()  
        
    def Ra1G_ModelView(self):
        self.model_R1G = QSqlTableModel(self.tableView_element)
        self.model_R1G.setTable('ra1_g')#设置要查询的表
        self.model_R1G.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_R1G.select()#使用表的数据填充模型
        self.model_R1G.setHeaderData(0, Qt.Horizontal, '位置(km)')
        self.model_R1G.setHeaderData(1, Qt.Horizontal, '阻抗值(kmΩ)')
        self.model_R1G.setFilter
        
        self.tableView_element.setModel(self.model_R1G)
        #self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        self.pushButton_add.clicked.connect(self.addR1G)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delR1G)#按减号删除一行
    def addR1G(self):
        rowNum =  self.model_R1G.rowCount()
        self.model_R1G.insertRow(rowNum)
        self.model_R1G.submitAll()
    def delR1G(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_R1G.removeRow(curRow)
        self.model_R1G.select()  
        
    def E1G_ModelView(self):
        self.model_E1G = QSqlTableModel(self.tableView_element)
        self.model_E1G.setTable('e1_g')#设置要查询的表
        self.model_E1G.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_E1G.select()#使用表的数据填充模型
        self.model_E1G.setHeaderData(0, Qt.Horizontal, '位置(km)')
        self.model_E1G.setHeaderData(1, Qt.Horizontal, '阻抗值(kmΩ)')
        self.model_E1G.setFilter
        
        self.tableView_element.setModel(self.model_E1G)
        #self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        
        self.pushButton_add.clicked.connect(self.addE1G)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delE1G)#按减号删除一行
    def addE1G(self):
        rowNum =  self.model_E1G.rowCount()
        self.model_E1G.insertRow(rowNum)
        self.model_E1G.submitAll()
    def delE1G(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_E1G.removeRow(curRow)
        self.model_E1G.select()  
        
    def Ra3G_ModelView(self):
        self.model_R3G = QSqlTableModel(self.tableView_element)
        self.model_R3G.setTable('ra3_g')#设置要查询的表
        self.model_R3G.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_R3G.select()#使用表的数据填充模型
        self.model_R3G.setHeaderData(0, Qt.Horizontal, '位置(km)')
        self.model_R3G.setHeaderData(1, Qt.Horizontal, '阻抗值(kmΩ)')
        self.model_R3G.setFilter
        
        self.tableView_element.setModel(self.model_R3G)
        #self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        
        self.pushButton_add.clicked.connect(self.addR3G)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delR3G)#按减号删除一行
    def addR3G(self):
        rowNum =  self.model_R3G.rowCount()
        self.model_R3G.insertRow(rowNum)
        self.model_R3G.submitAll()
    def delR3G(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_R3G.removeRow(curRow)
        self.model_R3G.select()  
        
    def E2G_ModelView(self):
        self.model_E2G = QSqlTableModel(self.tableView_element)
        self.model_E2G.setTable('e2_g')#设置要查询的表
        self.model_E2G.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_E2G.select()#使用表的数据填充模型
        self.model_E2G.setHeaderData(0, Qt.Horizontal, '位置(km)')
        self.model_E2G.setHeaderData(1, Qt.Horizontal, '阻抗值(kmΩ)')
        self.model_E2G.setFilter
        
        self.tableView_element.setModel(self.model_E2G)
        #self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        
        self.pushButton_add.clicked.connect(self.addE2G)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delE2G)#按减号删除一行
    def addE2G(self):
        rowNum =  self.model_E2G.rowCount()
        self.model_E2G.insertRow(rowNum)
        self.model_E2G.submitAll()
    def delE2G(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_E2G.removeRow(curRow)
        self.model_E2G.select()  
        
    def ParaR_ModelView(self):
        self.model_PR = QSqlTableModel(self.tableView_element)
        self.model_PR.setTable('para_resistance')#设置要查询的表
        self.model_PR.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model_PR.select()#使用表的数据填充模型
        self.model_PR.setHeaderData(0, Qt.Horizontal, '位置(km)')
        self.model_PR.setHeaderData(1, Qt.Horizontal, '阻抗值(kmΩ)')
        self.model_PR.setFilter
        
        self.tableView_element.setModel(self.model_PR)
        #self.tableView_element.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_element.show()#显示tableView的内容
        
        self.pushButton_add.clicked.connect(self.addPR)#按加号添加一行
        self.pushButton_del.clicked.connect(self.delPR)#按减号删除一行
    def addPR(self):
        rowNum =  self.model_PR.rowCount()
        self.model_PR.insertRow(rowNum)
        self.model_PR.submitAll()
    def delPR(self):
        curRow = self.tableView_element.currentIndex().row()
        self.model_PR.removeRow(curRow)
        self.model_PR.select()  
    
if __name__== "__main__":
    app = QApplication(sys.argv)
    Test = sql_set()
    
    
    Test.show()
    sys.exit(app.exec_())
    
