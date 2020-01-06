# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5.QtWidgets import QDialog, QApplication, QComboBox, QTableWidgetItem
from Ui_topology import Ui_Dialog
import pandas as pd
import numpy as np
#from qtpy.QtCore import Qt
from PyQt5.Qt import *
class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        #添加topology参数设置信号
        
        self.setWindowTitle("参数设置")
        
        self.checkBox1.setChecked(False)
        self.checkBox1.clicked.connect(self.Line)
        self.checkBox2.clicked.connect(self.Autotransformer)
        self.checkBox3.clicked.connect(self.Tractiontransformer)
        self.checkBox4.clicked.connect(self.to_all)
        self.checkBox5.clicked.connect(self.pw1_ra1)
        self.checkBox6.clicked.connect(self.e1_ra1)
        self.checkBox7.clicked.connect(self.e1_g)
        self.checkBox8.clicked.connect(self.pw2_ra3)
        self.checkBox9.clicked.connect(self.e2_ra3)
        self.checkBox10.clicked.connect(self.e2_g)
        self.checkBox11.clicked.connect(self.ra1_g)
        self.checkBox12.clicked.connect(self.ra3_g)
        self.checkBox13.clicked.connect(self.locomotive)
        
        btn_save1=QPushButton(self)
        btn_save1.move(40, 370)
        btn_save1.resize(101, 25)
        btn_save1.setText("保   存")
        btn_save1.clicked.connect(self.set_save1)####这边按钮名称前不需要加self.
        
    #添加topology参数设置槽函数   
    def Line(self):
        #self.tableWidget.clear()
        #self.pushButton1.clicked.connect(self.set_callback)
        #self.pushButton2.clicked.connect(self.set_call_look)
    #建表，插入导线名称
        input_table_rows = 14
        input_table_header = ['导线名称', '导线型号','导线坐标x(mm)', '导线坐标y(mm)', '计算截面积(mm2)', '单位质量（kg/km）', '导电率（S/m）', '持续载流量（A）', '计算半径(mm)', '等效半径(mm)','直流电阻(Ω)','相对磁导率(H/m)','电阻率*0.01777*10**-6(Ω*m)-1' ]
        input_table_colunms = len(input_table_header)##9列
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        #self.tableWidget.verticalHeader().setVisible(False)#隐藏垂直表头
        #self.tableWidget.horizontalHeader().setVisible(False)#隐藏水平表头
        line_name =  ['接触导线CW1', '承力索MW1', '正馈线PF1', '钢轨RA1', '钢轨RA2', '保护线PW1', '综合地线E1','接触导线CW2', '承力索MW2', '正馈线PF2', '钢轨RA3', '钢轨RA4', '保护线PW2', '综合地线E2' ]
        for i in range(14):
                temp_data = line_name[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(i,0,data)
        x_size = ['0', '0', '-4400', '-755', '755', '-3600', '-4400', '5000', '5000', '9400', '4245', '5755', '8600', '9400']
        y_size = ['6300', '7500', '8500', '1000', '1000', '8000', '500', '6300', '7500', '8500', '1000', '1000', '8000', '500']
        for i in range(14):
                temp_data = x_size[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(i,2,data)        
        for j in range(14):
                temp_data = y_size[j]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(j,3,data)        
            
        self.comBox1 = QComboBox()
        self.tableWidget.setCellWidget(0, 1, self.comBox1)
        self.comBox2 = QComboBox()
        self.tableWidget.setCellWidget(1, 1, self.comBox2)
        self.comBox3 = QComboBox()
        self.tableWidget.setCellWidget(2, 1, self.comBox3)
        self.comBox4 = QComboBox()
        self.tableWidget.setCellWidget(3, 1, self.comBox4)
        self.comBox5 = QComboBox()
        self.tableWidget.setCellWidget(4, 1, self.comBox5)
        self.comBox6 = QComboBox()
        self.tableWidget.setCellWidget(5, 1, self.comBox6)
        self.comBox7 = QComboBox()
        self.tableWidget.setCellWidget(6, 1, self.comBox7)
        self.comBox8 = QComboBox()
        self.tableWidget.setCellWidget(7, 1, self.comBox8)
        self.comBox9 = QComboBox()
        self.tableWidget.setCellWidget(8, 1, self.comBox9)   
        self.comBox10 = QComboBox()
        self.tableWidget.setCellWidget(9, 1, self.comBox10)  
        self.comBox11 = QComboBox()
        self.tableWidget.setCellWidget(10, 1, self.comBox11)
        self.comBox12 = QComboBox()
        self.tableWidget.setCellWidget(11, 1, self.comBox12)
        self.comBox13 = QComboBox()
        self.tableWidget.setCellWidget(12, 1, self.comBox13)
        self.comBox14 = QComboBox()
        self.tableWidget.setCellWidget(13, 1, self.comBox14)
        
        ##快速添加对应导线的导线型号类型
        from sqlite3 import connect
        db_name = 'test_source_lines.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('select * from star_lines')
        sqlcom1 = 'select name_line from star_lines'
        sqlcom2 = 'select model_line from star_lines'
        sqlcom3 = 'select area_line from star_lines'
        sqlcom4 = 'select m_line from star_lines'
        sqlcom5 = 'select rou_line from star_lines'
        sqlcom6 = 'select i_line from star_lines'
        sqlcom7 = 'select cal_r from star_lines'
        sqlcom8 = 'select q_r from star_lines'
        sqlcom9 = 'select Rd from star_lines'
        sqlcom10 = 'select mu_r from star_lines'
        sqlcom11 = 'select rho from star_lines'
        df1 = pd.read_sql(sqlcom1, con)
        df2 = pd.read_sql(sqlcom2, con)
        df3 = pd.read_sql(sqlcom3, con)
        df4 = pd.read_sql(sqlcom4, con)
        df5 = pd.read_sql(sqlcom5, con)
        df6 = pd.read_sql(sqlcom6, con)
        df7 = pd.read_sql(sqlcom7, con)
        df8 = pd.read_sql(sqlcom8, con)
        df9 = pd.read_sql(sqlcom9, con)
        df10 = pd.read_sql(sqlcom10, con)
        df11 = pd.read_sql(sqlcom11, con)
        
        df1 = np.array(df1)  # 先使用array()将DataFrame转换一下
        df2 = np.array(df2 )
        ff = np.hstack((df1, df2))
        ff = np.hstack((ff, df3))
        ff = np.hstack((ff, df4))
        ff = np.hstack((ff, df5))
        ff = np.hstack((ff, df6))
        ff = np.hstack((ff, df7))
        ff = np.hstack((ff, df8))
        ff = np.hstack((ff, df9))
        ff = np.hstack((ff, df10))
        ff = np.hstack((ff, df11))

        lines_data=ff
        print(lines_data)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        result =pd.DataFrame(columns=['导线名称', '导线型号', '计算截面积(mm2)', '单位质量（kg/km）', '导电率（S/m）', '持续载流量（A）', '计算半径(mm)', '等效半径(mm)', '直流电阻(Ω)','相对磁导率(H/m)','电阻率(Ω*m)-1'])
        print(result)
        for i in range(lines_data.shape[0]):
            s = pd.Series({'导线名称':lines_data[i][0],'导线型号':lines_data[i][1], '计算截面积(mm2)':lines_data[i][2], '单位质量（kg/km）':lines_data[i][3],'导电率（S/m）':lines_data[i][4]
               ,'持续载流量（A）':lines_data[i][5],'计算半径(mm)':lines_data[i][6],'等效半径(mm)':lines_data[i][7],'直流电阻(Ω)':lines_data[i][8],'相对磁导率(H/m)':lines_data[i][9],'电阻率(Ω*m)-1':lines_data[i][10]},name=lines_data[i][0])
            print(s)
            #result=result.append(s, ignore_index=True)
            result=result.append(s)
        print(result)
        print(result.index.tolist())
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        lines_data_frame=result
    #接触导线型号
        self.selected_frame_jiechuxian=lines_data_frame.loc['接触导线']
        self.selected_frame_jiechuxian_mult_model=self.selected_frame_jiechuxian['导线型号'].tolist()
        print(self.selected_frame_jiechuxian_mult_model)
    #承力索型号
        self.selected_frame_chenglisuo=lines_data_frame.loc['承力索']
        self.selected_frame_chenglisuo_mult_model=self.selected_frame_chenglisuo['导线型号'].tolist()
        print(self.selected_frame_chenglisuo_mult_model)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #正馈线型号(与承力索用相同的型号)
        self.selected_frame_zhengkuixian=lines_data_frame.loc['正馈线']
        self.selected_frame_zhengkuixian_mult_model=self.selected_frame_chenglisuo['导线型号'].tolist()
        print(self.selected_frame_zhengkuixian_mult_model)    
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #保护线型号
        self.selected_frame_baohuxian=lines_data_frame.loc['保护线']
        self.selected_frame_baohuxian_mult_model=self.selected_frame_baohuxian['导线型号'].tolist()
        print(self.selected_frame_baohuxian_mult_model)    
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')    
    #综合地线型号
        self.selected_frame_zonghedixian=lines_data_frame.loc['综合地线']
        self.selected_frame_zonghedixian_mult_model=self.selected_frame_zonghedixian['导线型号'].tolist()
        print(self.selected_frame_zonghedixian_mult_model)    
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')   
        
    #回流线或加强线
        self.selected_frame_huiliuxianhuojiaqiangxian=lines_data_frame.loc['回流线或加强线']
        self.selected_frame_huiliuxianhuojiaqiangxian_mult_model=self.selected_frame_huiliuxianhuojiaqiangxian['导线型号'].tolist()
        print(self.selected_frame_huiliuxianhuojiaqiangxian_mult_model)
    #钢轨
        self.selected_frame_ganggui=lines_data_frame.loc['钢轨']
        self.selected_frame_ganggui_mult_model=self.selected_frame_ganggui['导线型号'].tolist()
        print(self.selected_frame_ganggui_mult_model)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    #单一数据
        self.comBox1.addItems(self.selected_frame_jiechuxian_mult_model)
        self.comBox1.currentIndexChanged.connect(self.select1)
        self.comBox2.addItems(self.selected_frame_chenglisuo_mult_model)
        self.comBox2.currentIndexChanged.connect(self.select2)
        
        self.comBox3.addItems(self.selected_frame_zhengkuixian_mult_model)
        self.comBox3.currentIndexChanged.connect(self.select3)
        
        self.comBox4.addItems(self.selected_frame_ganggui_mult_model)
        self.comBox4.currentIndexChanged.connect(self.select4)
        self.comBox5.addItems(self.selected_frame_ganggui_mult_model)
        self.comBox5.currentIndexChanged.connect(self.select5)
        
        self.comBox6.addItems(self.selected_frame_baohuxian_mult_model)
        self.comBox6.currentIndexChanged.connect(self.select6)
        
        self.comBox7.addItems(self.selected_frame_zonghedixian_mult_model)
        self.comBox7.currentIndexChanged.connect(self.select7)
        
        self.comBox8.addItems(self.selected_frame_jiechuxian_mult_model)
        self.comBox8.currentIndexChanged.connect(self.select8)
        self.comBox9.addItems(self.selected_frame_chenglisuo_mult_model)
        self.comBox9.currentIndexChanged.connect(self.select9)
        
        self.comBox10.addItems(self.selected_frame_zhengkuixian_mult_model)
        self.comBox10.currentIndexChanged.connect(self.select10)
        
        self.comBox11.addItems(self.selected_frame_ganggui_mult_model)
        self.comBox11.currentIndexChanged.connect(self.select11)
        self.comBox12.addItems(self.selected_frame_ganggui_mult_model)
        self.comBox12.currentIndexChanged.connect(self.select12)
        
        self.comBox13.addItems(self.selected_frame_baohuxian_mult_model)
        self.comBox13.currentIndexChanged.connect(self.select13)
        self.comBox14.addItems(self.selected_frame_zonghedixian_mult_model)
        self.comBox14.currentIndexChanged.connect(self.select14)
        
    def select1(self):
        simple_data=self.selected_frame_jiechuxian[self.selected_frame_jiechuxian['导线型号'].isin([self.comBox1.currentText()])]
        print('-------------------------------------------------------')
        print(simple_data)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        simple_data_value=simple_data.values
        print(simple_data_value)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
        #print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        #print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(0,j+2,data)

    def select2(self):

        simple_data=self.selected_frame_chenglisuo[self.selected_frame_chenglisuo['导线型号'].isin([self.comBox2.currentText()])]
        #print('-------------------------------------------------------')
        #print('-------------------------------------------------------')
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        #print('-------------------------------------------------------')
        #print('-------------------------------------------------------')

        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(1,j+2,data)
    def select3(self):

        simple_data=self.selected_frame_zhengkuixian[self.selected_frame_zhengkuixian['导线型号'].isin([self.comBox3.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)

        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(2,j+2,data)
    
    def select4(self):

        simple_data=self.selected_frame_ganggui[self.selected_frame_ganggui['导线型号'].isin([self.comBox4.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(3,j+2,data)
    
    def select5(self):

        simple_data=self.selected_frame_ganggui[self.selected_frame_ganggui['导线型号'].isin([self.comBox5.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(4,j+2,data)
            
    def select6(self):

        simple_data=self.selected_frame_baohuxian[self.selected_frame_baohuxian['导线型号'].isin([self.comBox6.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(5,j+2,data)
            
    def select7(self):

        simple_data=self.selected_frame_zonghedixian[self.selected_frame_zonghedixian['导线型号'].isin([self.comBox7.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(6,j+2,data)
            
    
    def select8(self):

        simple_data=self.selected_frame_jiechuxian[self.selected_frame_jiechuxian['导线型号'].isin([self.comBox8.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(7,j+2,data)
    
    def select9(self):

        simple_data=self.selected_frame_chenglisuo[self.selected_frame_chenglisuo['导线型号'].isin([self.comBox9.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(8,j+2,data)
            
    def select10(self):

        simple_data=self.selected_frame_zhengkuixian[self.selected_frame_zhengkuixian['导线型号'].isin([self.comBox10.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(9,j+2,data)
            
    def select11(self):

        simple_data=self.selected_frame_ganggui[self.selected_frame_ganggui['导线型号'].isin([self.comBox11.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(10,j+2,data)
    
    def select12(self):

        simple_data=self.selected_frame_ganggui[self.selected_frame_ganggui['导线型号'].isin([self.comBox12.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(11,j+2,data)
    
    def select13(self):

        simple_data=self.selected_frame_baohuxian[self.selected_frame_baohuxian['导线型号'].isin([self.comBox13.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(12,j+2,data)
    
    def select14(self):

        simple_data=self.selected_frame_zonghedixian[self.selected_frame_zonghedixian['导线型号'].isin([self.comBox14.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 11):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(13,j+2,data)
        #self.btn_save1.clicked.connect(self.set_save1)###导线选择，加上初始值，否则可能报错，保存了空值
            
    #添加用于显示当前tablewidget表格中的数值槽函数        
    def set_save1(self):
        #插入一个判断的窗口，当存在空格时，显示存在空格
        #for i in range()
        total_data = []
        for i in range(14):
            row_data = []
            for j in range(2,13):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        print("---------------------------")
        print(total_data)
        print("----------------------------")
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_lines')  # 解决提示star已存在的问题
        cur.execute('create table star_lines(axis_x float,axis_y float,area_line float,m_line float, rou_line float,i_line float,cal_r float,q_r float,Rd float,mu_r float,rho float)')
        for item in total_data:
            cur.execute('insert into star_lines(axis_x,axis_y,area_line,m_line,rou_line,i_line,cal_r,q_r,Rd,mu_r,rho) values(?,?,?,?,?,?,?,?,?,?,?)',item)
        cur.execute('select * from star_lines')
        for row in cur:
                print(row)
        con.commit()
        con.close()
        
    ##AT变压器配置数据
    def Autotransformer(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        input_table_header = ['AT名称','AT型号', '位置(Km)', '漏导纳实部(Ω)','漏导纳虚部(Ω)' ]
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)


        btn_save2=QPushButton(self)
        btn_save2.move(40, 370)
        btn_save2.resize(101, 25)
        btn_save2.setText("保   存")
        btn_save2.show()
        btn_insert2=QPushButton(self)
        btn_insert2.move(40, 410)
        btn_insert2.resize(101, 25)
        btn_insert2.setText("添加一行")
        btn_insert2.show()
        
        btn_delete2=QPushButton(self)
        btn_delete2.move(40, 450)
        btn_delete2.resize(101, 25)
        btn_delete2.setText("删除一行")
        btn_delete2.show()
        
        line_name_d =  ['一号', 'vx', '0', '1', '1']###可替换为老师程序中的初始值
        for i in range(5):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert2.clicked.connect(self.table_insert2)
        btn_delete2.clicked.connect(self.table_delete2)
        btn_save2.clicked.connect(self.set_save2)
        
    def table_insert2(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
 
        item_id = QTableWidgetItem("一号")###可替换为老师程序中的初始值
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_id,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
 
        item_name = QTableWidgetItem("vx") #我们要求它可以修改，所以使用默认的状态即可###可替换为老师程序中的初始值
        
 
        item_location = QTableWidgetItem("0")###可替换为老师程序中的初始值
        
        #item_pos.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
        
        item_pos_real = QTableWidgetItem("1") #我们要求它可以修改，所以使用默认的状态即可###可替换为老师程序中的初始值
        
        #item_pos = QTableWidgetItem("1") #我们要求它可以修改，所以使用默认的状态即可###可替换为老师程序中的初始值
        item_pos_imag = QTableWidgetItem("1") #我们要求它可以修改，所以使用默认的状态即可###可替换为老师程序中的初始值
        
        self.tableWidget.setItem(row, 0, item_id)
        self.tableWidget.setItem(row, 1, item_name)
        self.tableWidget.setItem(row, 2, item_location)
        self.tableWidget.setItem(row, 3, item_pos_real)
        self.tableWidget.setItem(row, 4, item_pos_imag)
        
    def table_delete2(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
        
        
    def set_save2(self):
        total_data = []
        input_table_header = ['AT名称','AT型号', '位置(Km)', '漏导纳实部(Ω)','漏导纳虚部(Ω)' ]
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_AT')  # 解决提示star已存在的问题
        cur.execute('create table star_AT(name_AT text,model_AT text,location_AT float,lou_real float,lou_imag float)')
        for item in total_data:
            cur.execute('insert into star_AT(name_AT,model_AT,location_AT,lou_real,lou_imag) values(?,?,?,?,?)',item)
        cur.execute('select * from star_AT')
        for row in cur:
                print(row)
        con.commit()
        con.close()
        
        
        
    ##牵引变压器配置数据
    def Tractiontransformer(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        input_table_header = ['牵引变压器名称','牵引变压器型号', '位置(Km)','系统内阻抗实部(Ω)','系统内阻抗虚部(Ω)']
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        btn_save3=QPushButton(self)
        btn_save3.move(40, 370)
        btn_save3.resize(101, 25)
        btn_save3.setText("保   存")
        btn_save3.show()
        btn_insert3=QPushButton(self)
        btn_insert3.move(40, 410)
        btn_insert3.resize(101, 25)
        btn_insert3.setText("添加一行")
        btn_insert3.show()
        
        btn_delete3=QPushButton(self)
        btn_delete3.move(40, 450)
        btn_delete3.resize(101, 25)
        btn_delete3.setText("删除一行")
        btn_delete3.show()
        
        line_name_d =  ['一号', 'vx', '0', '1', '1']###可替换为老师程序中的初始值
        for i in range(5):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert3.clicked.connect(self.table_insert3)
        btn_delete3.clicked.connect(self.table_delete3)
        btn_save3.clicked.connect(self.set_save3)
        
    def table_insert3(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
 
        item_id = QTableWidgetItem("一号")###可替换为老师程序中的初始值
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_id,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
 
        item_name = QTableWidgetItem("vx") #我们要求它可以修改，所以使用默认的状态即可###可替换为老师程序中的初始值
 
        item_location = QTableWidgetItem("0")###可替换为老师程序中的初始值
        #item_pos.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
        
        item_pos_real = QTableWidgetItem("1") #我们要求它可以修改，所以使用默认的状态即可###可替换为老师程序中的初始值
        item_pos_imag = QTableWidgetItem("1") #我们要求它可以修改，所以使用默认的状态即可###可替换为老师程序中的初始值
        
        self.tableWidget.setItem(row, 0, item_id)
        self.tableWidget.setItem(row, 1, item_name)
        self.tableWidget.setItem(row, 2, item_location)
        self.tableWidget.setItem(row, 3, item_pos_real)
        self.tableWidget.setItem(row, 3, item_pos_imag)
        
        
    def table_delete3(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
    def set_save3(self):
        total_data = []
        input_table_header = ['牵引变压器名称','牵引变压器型号', '位置(Km)','系统内阻抗实部(Ω)','系统内阻抗虚部(Ω)']
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_qianyin')  # 解决提示star已存在的问题
        cur.execute('create table star_qianyin(name_qianyin text,model_qianyin text,location_qianyin float,neizukang_qianyin_real float,neizukang_qianyin_imag float)')
        for item in total_data:
            cur.execute('insert into star_qianyin(name_qianyin,model_qianyin,location_qianyin,neizukang_qianyin_real,neizukang_qianyin_imag) values(?,?,?,?,?)',item)
        cur.execute('select * from star_qianyin')
        for row in cur:
                print(row)
        con.commit()
        con.close()
        
        ##上下行并联线配置数据
    def to_all(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        #input_table_header = ['上行导线（0、1、2）','下行导线（3、4、5）','位置(Km)']
        input_table_header = ['位置(Km)']
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        btn_save4=QPushButton(self)
        btn_save4.move(40, 370)
        btn_save4.resize(101, 25)
        btn_save4.setText("保   存")
        btn_save4.show()
        btn_insert4=QPushButton(self)
        btn_insert4.move(40, 410)
        btn_insert4.resize(101, 25)
        btn_insert4.setText("添加一行")
        btn_insert4.show()
        
        btn_delete4=QPushButton(self)
        btn_delete4.move(40, 450)
        btn_delete4.resize(101, 25)
        btn_delete4.setText("删除一行")
        btn_delete4.show()
        
        line_name_d =  [ '0']###可替换为老师程序中的初始值
        for i in range(1):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert4.clicked.connect(self.table_insert4)
        btn_delete4.clicked.connect(self.table_delete4)
        btn_save4.clicked.connect(self.set_save4)
        
    def table_insert4(self):
        #self.tableWidget.clear()###清空上一个表格的数据
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
 
        #item_up = QTableWidgetItem("1")###可替换为老师程序中的初始值
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_id,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
 
        #item_down = QTableWidgetItem("4") #我们要求它可以修改，所以使用默认的状态即可###可替换为老师程序中的初始值
 
        item_location = QTableWidgetItem("0")###可替换为老师程序中的初始值
        #item_pos.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
        
        
        #self.tableWidget.setItem(row, 0, item_up)
        #self.tableWidget.setItem(row, 1, item_down)
        self.tableWidget.setItem(row,0, item_location)
        
    def table_delete4(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
    def set_save4(self):
        total_data = []
        input_table_header = ['位置(Km)']
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_up_down')  # 解决提��star已存在的问题
        cur.execute('create table star_up_down(location_star_up_down float)')
        for item in total_data:
            cur.execute('insert into star_up_down(location_star_up_down) values(?)',item)
        cur.execute('select * from star_up_down')
        for row in cur:
                print(row)
        con.commit()
        con.close()
        
    ##pw1_ra1配置数据
    def pw1_ra1(self):
        #self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        input_table_header = ['位置(Km)']
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        btn_save5=QPushButton(self)
        btn_save5.move(40, 370)
        btn_save5.resize(101, 25)
        btn_save5.setText("保   存")
        btn_save5.show()
        btn_insert5=QPushButton(self)
        btn_insert5.move(40, 410)
        btn_insert5.resize(101, 25)
        btn_insert5.setText("添加一行")
        btn_insert5.show()
        
        btn_delete5=QPushButton(self)
        btn_delete5.move(40, 450)
        btn_delete5.resize(101, 25)
        btn_delete5.setText("删除一行")
        btn_delete5.show()
        
        line_name_d =  ['1']###可替换为老师程序中的初始值
        for i in range(1):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert5.clicked.connect(self.table_insert5)
        btn_delete5.clicked.connect(self.table_delete5)
        btn_save5.clicked.connect(self.set_save5)
        
    def table_insert5(self):
        #self.tableWidget.clear()###清空上一个表格的数据
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
 
        item_location = QTableWidgetItem("1")###可替换为老师程序中的初始值
        self.tableWidget.setItem(row, 0, item_location)
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_id,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        #self.tableWidget.setItem(row, 0, item_location)
        #self.pushButton1.clicked.connect(self.set_save2)
        
    def table_delete5(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
    def set_save5(self):
        total_data = []
        input_table_header = ['位置(Km)']
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_pw1_ra1')  # 解决提��star已存在的问题
        cur.execute('create table star_pw1_ra1(location_star_pw1_ra1 float)')
        for item in total_data:
            cur.execute('insert into star_pw1_ra1(location_star_pw1_ra1) values(?)',item)
        cur.execute('select * from star_pw1_ra1')
        for row in cur:
                print(row)
        con.commit()
        con.close()     
        
    ##e1_ra1配置数据
    def e1_ra1(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        input_table_header = ['位置(Km)']
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        btn_save6=QPushButton(self)
        btn_save6.move(40, 370)
        btn_save6.resize(101, 25)
        btn_save6.setText("保   存")
        btn_save6.show()
        btn_insert6=QPushButton(self)
        btn_insert6.move(40, 410)
        btn_insert6.resize(101, 25)
        btn_insert6.setText("添加一行")
        btn_insert6.show()
        
        btn_delete6=QPushButton(self)
        btn_delete6.move(40, 450)
        btn_delete6.resize(101, 25)
        btn_delete6.setText("删除一行")
        btn_delete6.show()
        
        line_name_d =  ['1']###可替换为老师程序中的初始值
        for i in range(1):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert6.clicked.connect(self.table_insert6)
        btn_delete6.clicked.connect(self.table_delete6)
        btn_save6.clicked.connect(self.set_save6)
        
    def table_insert6(self):
        #self.tableWidget.clear()###清空上一个表格的数据
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
 
        item_location = QTableWidgetItem("1")###可替换为老师程序中的初始值
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_id,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        self.tableWidget.setItem(row, 0, item_location)
        #self.pushButton1.clicked.connect(self.set_save2)
        
    def table_delete6(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
    def set_save6(self):
        total_data = []
        input_table_header = ['位置(Km)']
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_e1_ra1')  # 解决提��star已存在的问题
        cur.execute('create table star_e1_ra1(location_star_e1_ra1 float)')
        for item in total_data:
            cur.execute('insert into star_e1_ra1(location_star_e1_ra1) values(?)',item)
        cur.execute('select * from star_e1_ra1')
        for row in cur:
                print(row)
        con.commit()
        con.close() 
        
    ##e1_g配置数据
    def e1_g(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        input_table_header = ['位置(Km)', '阻抗值(Km.Ω)' ]
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        btn_save7=QPushButton(self)
        btn_save7.move(40, 370)
        btn_save7.resize(101, 25)
        btn_save7.setText("保   存")
        btn_save7.show()
        btn_insert7=QPushButton(self)
        btn_insert7.move(40, 410)
        btn_insert7.resize(101, 25)
        btn_insert7.setText("添加一行")
        btn_insert7.show()
        
        btn_delete7=QPushButton(self)
        btn_delete7.move(40, 450)
        btn_delete7.resize(101, 25)
        btn_delete7.setText("删除一行")
        btn_delete7.show()
        
        line_name_d =  ['2', '0.001']###可替换为老师程序中的初始值
        for i in range(2):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert7.clicked.connect(self.table_insert7)
        btn_delete7.clicked.connect(self.table_delete7)
        btn_save7.clicked.connect(self.set_save7)
        
    def table_insert7(self):
        #self.tableWidget.clear()###清空上一个表格的数据
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
 
        item_location = QTableWidgetItem('2')###可替换为老师程序中的初始值
        item_zukang = QTableWidgetItem('0.001')###可替换为老师程序中的初始值
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_id,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        self.tableWidget.setItem(row, 0, item_location)
        self.tableWidget.setItem(row, 1, item_zukang)
        #self.pushButton1.clicked.connect(self.set_save2)
        
    def table_delete7(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
    def set_save7(self):
        total_data = []
        input_table_header = ['位置(Km)', '阻抗值(Km.Ω)']
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_e1_g')  # 解决提��star已存在的问题
        cur.execute('create table star_e1_g(location_star_e1_g float,Z_star_e1_g float)')
        for item in total_data:
            cur.execute('insert into star_e1_g(location_star_e1_g,Z_star_e1_g) values(?,?)',item)
        cur.execute('select * from star_e1_g')
        for row in cur:
                print(row)
        con.commit()
        con.close()      
        
    ##pw2_ra3配置数据
    def pw2_ra3(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        input_table_header = ['位置(Km)']
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        btn_save8=QPushButton(self)
        btn_save8.move(40, 370)
        btn_save8.resize(101, 25)
        btn_save8.setText("保   存")
        btn_save8.show()
        btn_insert8=QPushButton(self)
        btn_insert8.move(40, 410)
        btn_insert8.resize(101, 25)
        btn_insert8.setText("添加一行")
        btn_insert8.show()
        
        btn_delete8=QPushButton(self)
        btn_delete8.move(40, 450)
        btn_delete8.resize(101, 25)
        btn_delete8.setText("删除一行")
        btn_delete8.show()
        
        line_name_d =  ['1']###可替换为老师程序中的初始值
        for i in range(1):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert8.clicked.connect(self.table_insert8)
        btn_delete8.clicked.connect(self.table_delete8)
        btn_save8.clicked.connect(self.set_save8)
        
    def table_insert8(self):
        #self.tableWidget.clear()###清空上一个表格的数据
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
 
        item_location = QTableWidgetItem("1")###可替换为老师程序中的初始值
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_location,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        self.tableWidget.setItem(row, 0, item_location)
        #self.pushButton1.clicked.connect(self.set_save2)
        
    def table_delete8(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
    def set_save8(self):
        total_data = []
        input_table_header = ['位置(Km)']
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_pw2_ra3')  # 解决提��star已存在的问题
        cur.execute('create table star_pw2_ra3(location_star_pw2_ra3 float)')
        for item in total_data:
            cur.execute('insert into star_pw2_ra3(location_star_pw2_ra3) values(?)',item)
        cur.execute('select * from star_pw2_ra3')
        for row in cur:
                print(row)
        con.commit()
        con.close()           
        
    ##e2_ra3配置数据
    def e2_ra3(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        input_table_header = ['位置(Km)']
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        btn_save9=QPushButton(self)
        btn_save9.move(40, 370)
        btn_save9.resize(101, 25)
        btn_save9.setText("保   存")
        btn_save9.show()
        btn_insert9=QPushButton(self)
        btn_insert9.move(40, 410)
        btn_insert9.resize(101, 25)
        btn_insert9.setText("添加一行")
        btn_insert9.show()
        
        btn_delete9=QPushButton(self)
        btn_delete9.move(40, 450)
        btn_delete9.resize(101, 25)
        btn_delete9.setText("删除一行")
        btn_delete9.show()
        
        line_name_d =  ['1']###可替换为老师程序中的初始值
        for i in range(1):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert9.clicked.connect(self.table_insert9)
        btn_delete9.clicked.connect(self.table_delete9)
        btn_save9.clicked.connect(self.set_save9)
        
    def table_insert9(self):
        #self.tableWidget.clear()###清空上一个表格的数据
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
 
        item_location = QTableWidgetItem("1")###可替换为老师程序中的初始值
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_id,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        self.tableWidget.setItem(row, 0, item_location)
        #self.pushButton1.clicked.connect(self.set_save2)
        
    def table_delete9(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
    def set_save9(self):
        total_data = []
        input_table_header = ['位置(Km)']
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_e2_ra3')  # 解决提��star已存在的问题
        cur.execute('create table star_e2_ra3(location_star_e2_ra3 float)')
        for item in total_data:
            cur.execute('insert into star_e2_ra3(location_star_e2_ra3) values(?)',item)
        cur.execute('select * from star_e2_ra3')
        for row in cur:
                print(row)
        con.commit()
        con.close()     
        
    ##e2_g配置数据
    def e2_g(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        input_table_header = ['位置(Km)', '阻抗值(Km.Ω)' ]
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        btn_save10=QPushButton(self)
        btn_save10.move(40, 370)
        btn_save10.resize(101, 25)
        btn_save10.setText("保   存")
        btn_save10.show()
        btn_insert10=QPushButton(self)
        btn_insert10.move(40, 410)
        btn_insert10.resize(101, 25)
        btn_insert10.setText("添加一行")
        btn_insert10.show()
        
        btn_delete10=QPushButton(self)
        btn_delete10.move(40, 450)
        btn_delete10.resize(101, 25)
        btn_delete10.setText("删除一行")
        btn_delete10.show()
        
        line_name_d =  ['2', '0.001']###可替换为老师程序中的初始值
        for i in range(2):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert10.clicked.connect(self.table_insert10)
        btn_delete10.clicked.connect(self.table_delete10)
        btn_save10.clicked.connect(self.set_save10)
        
    def table_insert10(self):
        #self.tableWidget.clear()###清空上一个表格的数据
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
 
        item_location = QTableWidgetItem('2')###可替换为老师程序中的初始值
        item_zukang = QTableWidgetItem('0.001')###可替换为老师程序中的初始值
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_id,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        self.tableWidget.setItem(row, 0, item_location)
        self.tableWidget.setItem(row, 1, item_zukang)
        #self.pushButton1.clicked.connect(self.set_save2)
        
    def table_delete10(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
    def set_save10(self):
        total_data = []
        input_table_header = ['位置(Km)', '阻抗值(Km.Ω)']
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_e2_g')  # 解决提��star已存在的问题
        cur.execute('create table star_e2_g(location_star_e2_g float,Z_star_e2_g float)')
        for item in total_data:
            cur.execute('insert into star_e2_g(location_star_e2_g,Z_star_e2_g) values(?,?)',item)
        cur.execute('select * from star_e2_g')
        for row in cur:
                print(row)
        con.commit()
        con.close()        
       
      
    ##ra1_g配置数据
    def ra1_g(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        input_table_header = ['位置(Km)', '阻抗值(Km.Ω)' ]
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        btn_save11=QPushButton(self)
        btn_save11.move(40, 370)
        btn_save11.resize(101, 25)
        btn_save11.setText("保   存")
        btn_save11.show()
        btn_insert11=QPushButton(self)
        btn_insert11.move(40, 410)
        btn_insert11.resize(101, 25)
        btn_insert11.setText("添加一行")
        btn_insert11.show()
        
        btn_delete11=QPushButton(self)
        btn_delete11.move(40, 450)
        btn_delete11.resize(101, 25)
        btn_delete11.setText("删除一行")
        btn_delete11.show()
        
        line_name_d =  ['2', '0.001']###可替换为老师程序中的初始值
        for i in range(2):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert11.clicked.connect(self.table_insert11)
        btn_delete11.clicked.connect(self.table_delete11)
        btn_save11.clicked.connect(self.set_save11)
        
    def table_insert11(self):
        #self.tableWidget.clear()###清空上一个表格的数据
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
 
        item_location = QTableWidgetItem('2')###可替换为老师程序中的初始值
        item_zukang = QTableWidgetItem('0.001')###可替换为老师程序中的初始值
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_id,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        self.tableWidget.setItem(row, 0, item_location)
        self.tableWidget.setItem(row, 1, item_zukang)
        #self.pushButton1.clicked.connect(self.set_save2)
        
    def table_delete11(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
    def set_save11(self):
        total_data = []
        input_table_header = ['位置(Km)', '阻抗值(Km.Ω)']
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_ra1_g')  # 解决提��star已存在的问题
        cur.execute('create table star_ra1_g(location_star_ra1_g float,Z_star_ra1_g float)')
        for item in total_data:
            cur.execute('insert into star_ra1_g(location_star_ra1_g,Z_star_ra1_g) values(?,?)',item)
        cur.execute('select * from star_ra1_g')
        for row in cur:
                print(row)
        con.commit()
        con.close()     
  

    ##ra3_g配置数据
    def ra3_g(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 1
        input_table_header = ['位置(Km)', '阻抗值(Km.Ω)' ]
        input_table_colunms = len(input_table_header)
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        btn_save12=QPushButton(self)
        btn_save12.move(40, 370)
        btn_save12.resize(101, 25)
        btn_save12.setText("保   存")
        btn_save12.show()
        btn_insert12=QPushButton(self)
        btn_insert12.move(40, 410)
        btn_insert12.resize(101, 25)
        btn_insert12.setText("添加一行")
        btn_insert12.show()
        
        btn_delete12=QPushButton(self)
        btn_delete12.move(40, 450)
        btn_delete12.resize(101, 25)
        btn_delete12.setText("删除一行")
        btn_delete12.show()
        
        line_name_d =  ['2', '0.001']###可替换为老师程序中的初始值
        for i in range(2):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(0, i,data)
        btn_insert12.clicked.connect(self.table_insert12)
        btn_delete12.clicked.connect(self.table_delete12)
        btn_save12.clicked.connect(self.set_save12)
        
    def table_insert12(self):
        #self.tableWidget.clear()###清空上一个表格的数据
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        item_location = QTableWidgetItem('2')###可替换为老师程序中的初始值
        item_zukang = QTableWidgetItem('0.001')###可替换为老师程序中的初始值
        #self.item_id.setTextAlignment(Qt.AlignCenter)
        #self.tableWidget.setTextAlignment(item_id,Qt.AlignVCenter)
        #item_id.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
        self.tableWidget.setItem(row, 0, item_location)
        self.tableWidget.setItem(row, 1, item_zukang)
        #self.pushButton1.clicked.connect(self.set_save2)
        
    def table_delete12(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        #self.pushButton1.clicked.connect(self.set_save2)
    def set_save12(self):
        total_data = []
        input_table_header = ['位置(Km)', '阻抗值(Km.Ω)']
        input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(input_table_colunms):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        #print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_ra3_g')  # 解决提��star已存在的问题
        cur.execute('create table star_ra3_g(location_star_ra3_g float,Z_star_ra3_g float)')
        for item in total_data:
            cur.execute('insert into star_ra3_g(location_star_ra3_g,Z_star_ra3_g) values(?,?)',item)
        cur.execute('select * from star_ra3_g')
        for row in cur:
                print(row)
        con.commit()
        con.close()         
    
    
    def locomotive(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 4
        input_table_header = ['属性','机车1', '机车2', '机车3', '机车4', '机车5']
        #input_table_colunms = len(input_table_header)##2列
        #self.tableWidget.setColumnCount(input_table_colunms)
        #self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        self.tableWidget.setVerticalHeaderLabels(input_table_header)
        
        
        input_table_colunms = 6##2列
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        #self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        
        self.tableWidget.verticalHeader().setVisible(False)#隐藏垂直表头
        #self.tableWidget.horizontalHeader().setVisible(False)#隐藏水平表头

        
        btn_save13=QPushButton(self)
        btn_save13.move(40, 370)
        btn_save13.resize(101, 25)
        btn_save13.setText("保   存")
        btn_save13.show()
        
        #btn_insert13_num=QPushButton(self)
        #btn_insert13_num.move(40, 410)
        #btn_insert13_num.resize(101, 25)
        #btn_insert13_num.setText("添加机车")
        #btn_insert13_num.show()
        
        btn_insert13_column=QPushButton(self)
        btn_insert13_column.move(40, 410)
        btn_insert13_column.resize(101, 25)
        btn_insert13_column.setText("添加谐波")
        btn_insert13_column.show()
        
        btn_delete13_row=QPushButton(self)
        btn_delete13_row.move(40, 450)
        btn_delete13_row.resize(101, 25)
        btn_delete13_row.setText("删除谐波")
        btn_delete13_row.show()
        
        #btn_delete13_column=QPushButton(self)
        #btn_delete13_column.move(40, 530)
        #btn_delete13_column.resize(101, 25)
        #btn_delete13_column.setText("删除机车")
        #btn_delete13_column.show()
        
        line_name =  ['位置(Km)','取流(A)','上下行（1为上行，0为下行）','1']
        #self.tableWidget.setVerticalHeaderLabels(['位置(Km)','取流(A)','上下行','一次谐波'])

        for i in range(4):
                temp_data = line_name[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(i,0,data)
        
        line_name_d =  ['5', '800','1',  '2%']###可替换为老师程序中的初始值
        for i in range(4):
                temp_data = line_name_d[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(i, 1, data)
                
        line_name_f =  ['0', '0','0',  '0']###可替换为老师程序中的初始值
        for i in range(4):
            for j in range(2, 6):
                    temp_data = line_name_f[i]  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)        
        #btn_insert13_num.clicked.connect(self.table_insert13_num)
        btn_insert13_column.clicked.connect(self.table_insert13_column)
        btn_delete13_row.clicked.connect(self.table_delete13_row)
        #btn_delete13_column.clicked.connect(self.table_delete13_column)
        btn_save13.clicked.connect(self.set_save13)

    def table_insert13_num(self):
        column = self.tableWidget.columnCount()
        
        #if column == 6:
            #return 
        
        self.tableWidget.insertColumn(column)
        item_current = QTableWidgetItem("800")
        item_location = QTableWidgetItem("5")
        item_up_down = QTableWidgetItem("1")
        item_xiebo = QTableWidgetItem("2%")
        self.tableWidget.setItem(0, column, item_location)
        self.tableWidget.setItem(1, column, item_current)
        self.tableWidget.setItem(2, column, item_up_down)
        self.tableWidget.setItem(3, column, item_xiebo)
        
    def table_insert13_column(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        item_many = QTableWidgetItem("1")###可替换为老师程序中的初始值
        item_1 = QTableWidgetItem("0")###可替换为老师程序中的初始值
        item_2 = QTableWidgetItem("0")###可替换为老师程序中的初始值
        item_3 = QTableWidgetItem("0")###可替换为老师程序中的初始值
        item_4 = QTableWidgetItem("0")###可替换为老师程序中的初始值
        item_5 = QTableWidgetItem("0")###可替换为老师程序中的初始值
        self.tableWidget.setItem(row, 0, item_many)
        self.tableWidget.setItem(row, 1, item_1)
        self.tableWidget.setItem(row, 2, item_2)
        self.tableWidget.setItem(row, 3, item_3)
        self.tableWidget.setItem(row, 4, item_4)
        self.tableWidget.setItem(row, 5, item_5)
        
    def table_delete13_row(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)    
        
    def table_delete13_column(self):
        column_select = self.tableWidget.selectedItems()
        if len(column_select) == 0:
            return
        id = column_select[0].text()
        print("id: {}".format(id))
 
        column = column_select[0].column()
        self.tableWidget.removeColumn(column)    
    

    def set_save13(self):
        total_data = []
        #input_table_header = ['位置(Km)', '阻抗值(Km.Ω)']
        #input_table_colunms = len(input_table_header)
        
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(self.tableWidget.columnCount()):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        print("上显示total_data")
        print(total_data)
        print("上显示total_data")
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_locomotive')  # 解决提��star已存在的问题
        cur.execute('create table star_locomotive(names_star_locomotive text,locomotive1_star_locomotive float,locomotive2_star_locomotive float,locomotive3_star_locomotive float,locomotive4_star_locomotive float,locomotive5_star_locomotive float)')
        for item in total_data:
            cur.execute('insert into star_locomotive(names_star_locomotive,locomotive1_star_locomotive,locomotive2_star_locomotive,locomotive3_star_locomotive,locomotive4_star_locomotive,locomotive5_star_locomotive) values(?,?,?,?,?,?)',item)
        cur.execute('select * from star_locomotive')
        for row in cur:
                print(row)
        con.commit()
        con.close()         


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Dialog()
    form.show()
    app.exec_()  
