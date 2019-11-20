# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QComboBox
from Ui_Line import Ui_Dialog
import pandas as pd
import numpy as np

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
        self.pushButton1.clicked.connect(self.set_callback)
        self.pushButton2.clicked.connect(self.set_call_look)
    #建表，插入导线名称
        input_table_rows = 14
        input_table_header = ['导线名称', '导线型号', '计算截面积(mm2)', '单位质量（kg/km）', '导电率（S/m）', '持续载流量（A）', '计算半径(mm)', '等效半径(mm)', '导线坐标x(mm)', '导线坐标y(mm)']
        input_table_colunms = len(input_table_header)##8列
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        line_name =  ['接触导线CW1', '承力索MW1', '正馈线PF1', '钢轨RA1', '钢轨RA2', '保护线PW1', '综合地线E1','接触导线CW2', '承力索MW2', '正馈线PF2', '钢轨RA3', '钢轨RA4', '保护线PW2', '综合地线E2' ]
        for i in range(14):
                temp_data = line_name[i]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                self.tableWidget.setItem(i,0,data)
        
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
        df1 = pd.read_sql(sqlcom1, con)
        df2 = pd.read_sql(sqlcom2, con)
        df3 = pd.read_sql(sqlcom3, con)
        df4 = pd.read_sql(sqlcom4, con)
        df5 = pd.read_sql(sqlcom5, con)
        df6 = pd.read_sql(sqlcom6, con)
        df7 = pd.read_sql(sqlcom7, con)
        df8 = pd.read_sql(sqlcom8, con)
        df1 = np.array(df1)  # 先使用array()将DataFrame转换一下
        df2 = np.array(df2 )
        ff = np.hstack((df1, df2))
        ff = np.hstack((ff, df3))
        ff = np.hstack((ff, df4))
        ff = np.hstack((ff, df5))
        ff = np.hstack((ff, df6))
        ff = np.hstack((ff, df7))
        ff = np.hstack((ff, df8))

        lines_data=ff
        print(lines_data)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        result =pd.DataFrame(columns=['导线名称', '导线型号', '计算截面积(mm2)', '单位质量（kg/km）', '导电率（S/m）', '持续载流量（A）', '计算半径(mm)', '等效半径(mm)'])
        print(result)
        
        for i in range(lines_data.shape[0]):
            s = pd.Series({'导线名称':lines_data[i][0],'导线型号':lines_data[i][1], '计算截面积(mm2)':lines_data[i][2], '单位质量（kg/km）':lines_data[i][3],'导电率（S/m）':lines_data[i][4]
               ,'持续载流量（A）':lines_data[i][5],'计算半径(mm)':lines_data[i][6],'等效半径(mm)':lines_data[i][7]},name=lines_data[i][0])
            print(s)
            #result=result.append(s, ignore_index=True)
            result=result.append(s)
        print(result)
        print(result.index.tolist())
        lines_data_frame=result
    #接触导线型号
        self.selected_frame_jiechuxian=lines_data_frame.loc['接触导线']
        self.selected_frame_jiechuxian_mult_model=self.selected_frame_jiechuxian['导线型号'].tolist()
        print(self.selected_frame_jiechuxian_mult_model)
    #承力索型号
        self.selected_frame_chenglisuo=lines_data_frame.loc['承力索']
        self.selected_frame_chenglisuo_mult_model=self.selected_frame_chenglisuo['导线型号'].tolist()
        print(self.selected_frame_chenglisuo_mult_model)
    #回流线或加强线
        self.selected_frame_huiliuxianhuojiaqiangxian=lines_data_frame.loc['回流线或加强线']
        self.selected_frame_huiliuxianhuojiaqiangxian_mult_model=self.selected_frame_huiliuxianhuojiaqiangxian['导线型号'].tolist()
        print(self.selected_frame_huiliuxianhuojiaqiangxian_mult_model)
    #钢轨
        self.selected_frame_ganggui=lines_data_frame.loc['钢轨']
        self.selected_frame_ganggui_mult_model=self.selected_frame_ganggui['导线型号'].tolist()
        print(self.selected_frame_ganggui_mult_model)
    #单一数据
        self.comBox1.addItems(self.selected_frame_jiechuxian_mult_model)
        self.comBox1.currentIndexChanged.connect(self.select1)
        self.comBox2.addItems(self.selected_frame_chenglisuo_mult_model)
        self.comBox2.currentIndexChanged.connect(self.select2)
        self.comBox4.addItems(self.selected_frame_ganggui_mult_model)
        self.comBox4.currentIndexChanged.connect(self.select4)
        self.comBox5.addItems(self.selected_frame_ganggui_mult_model)
        self.comBox5.currentIndexChanged.connect(self.select5)
        
        self.comBox8.addItems(self.selected_frame_jiechuxian_mult_model)
        self.comBox8.currentIndexChanged.connect(self.select8)
        self.comBox9.addItems(self.selected_frame_chenglisuo_mult_model)
        self.comBox9.currentIndexChanged.connect(self.select9)
        self.comBox11.addItems(self.selected_frame_ganggui_mult_model)
        self.comBox11.currentIndexChanged.connect(self.select10)
        self.comBox12.addItems(self.selected_frame_ganggui_mult_model)
        self.comBox12.currentIndexChanged.connect(self.select11)
    def select1(self):
        simple_data=self.selected_frame_jiechuxian[self.selected_frame_jiechuxian['导线型号'].isin([self.comBox1.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)

        for j in range(2, 8):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(0,j,data)

    def select2(self):

        simple_data=self.selected_frame_chenglisuo[self.selected_frame_chenglisuo['导线型号'].isin([self.comBox2.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)

        for j in range(2, 8):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(1,j,data)
            
    def select4(self):

        simple_data=self.selected_frame_ganggui[self.selected_frame_ganggui['导线型号'].isin([self.comBox4.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 8):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(3,j,data)
    
    def select5(self):

        simple_data=self.selected_frame_ganggui[self.selected_frame_ganggui['导线型号'].isin([self.comBox5.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 8):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(4,j,data)
            
    
    def select8(self):

        simple_data=self.selected_frame_jiechuxian[self.selected_frame_jiechuxian['导线型号'].isin([self.comBox8.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 8):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(7,j,data)
    
    def select9(self):

        simple_data=self.selected_frame_chenglisuo[self.selected_frame_chenglisuo['导线型号'].isin([self.comBox9.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 8):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(8,j,data)
            
    def select10(self):

        simple_data=self.selected_frame_ganggui[self.selected_frame_ganggui['导线型号'].isin([self.comBox11.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 8):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(10,j,data)
    
    def select11(self):

        simple_data=self.selected_frame_ganggui[self.selected_frame_ganggui['导线型号'].isin([self.comBox12.currentText()])]
        print(simple_data)
        simple_data_value=simple_data.values
        print(simple_data_value)
        
        for j in range(2, 8):
            temp_data = simple_data_value[0][j]  # 临时记录，不能直接插入表格
            data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
            self.tableWidget.setItem(11,j,data)
    #添加用于显示当前tablewidget表格中的数值槽函数        
    def set_callback(self):
        #插入一个判断的窗口，当存在空格时，显示存在空格
        #for i in range()
        total_data = []
        for i in range(14):
            row_data = []
            for j in range(2,10):
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
        cur.execute('create table star_lines(area_line float,m_line float, rou_line float,i_line float,cal_r float,q_r float,aixs_x float,axis_y float)')
        for item in total_data:
            cur.execute('insert into star_lines(area_line,m_line,rou_line,i_line,cal_r,q_r,aixs_x,axis_y) values(?,?,?,?,?,?,?,?)',item)
        cur.execute('select * from star_lines')
        for row in cur:
                print(row)
        con.commit()
        con.close()
    def set_call_look(self):
        pass

    
    

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Dialog()
    form.show()
    app.exec_() 
