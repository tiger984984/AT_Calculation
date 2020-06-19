# -*- coding: utf-8 -*-

"""
Module implementing Form.
"""

from PyQt5.QtWidgets import QWidget

from Ui_Line_change_source import Ui_Form


class Form(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Form, self).__init__(parent)
        self.setupUi(self)
# -*- coding: utf-8 -*-

"""
Module implementing Form.
"""
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QApplication

from Ui_Line_change_source import Ui_Form
from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np

class Form(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Form, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("牵引网参数管理")
        self.pushButton_1.clicked.connect(self.load_1)
        self.pushButton_2.clicked.connect(self.table_insert)
        self.pushButton_3.clicked.connect(self.table_delete)
        self.pushButton_4.clicked.connect(self.table_save)
    def load_1(self):
        from sqlite3 import connect
        db_name = 'source_lines.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('select * from lines')
        sqlcom1 = 'select line_name from lines'
        sqlcom2 = 'select line_mode from lines'
        sqlcom3 = 'select line_area from lines'
        sqlcom4 = 'select line_unit_mass from lines'
        sqlcom5 = 'select line_conductivity from lines'
        sqlcom6 = 'select line_Current_density from lines'
        sqlcom7 = 'select line_Calculation_radius from lines'
        sqlcom8 = 'select line_Equivalent_radius from lines'
        sqlcom9 = 'select line_Dc_resistance from lines'
        sqlcom10 = 'select line_Magnetic_permeability from lines'
        sqlcom11 = 'select line_Relative_permeability from lines'
        
        
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
        
        rows_1 = cur.fetchall()
        a = int(len(rows_1))
        vol = len(rows_1[0])  # 取得字段数，用于设置表格的列数
        self.tableWidget.setRowCount(a)
        self.tableWidget.setColumnCount(vol)
        self.tableWidget.setHorizontalHeaderLabels(['序号', '导线名称', '导线型号', '计算截面积（mm2）','单位质量（kg/km）', '导电率（S/m）', '持续载流量（A）', '计算半径(mm)', '等效半径(mm)', '直流电阻(Ω)', '磁导率（H/m）', '相对磁导率（H/m）'])
        
        #self.tableWidget.setColumnWidth(0, 40)
        for i in range(a):
            for j in range(vol):
                temp_data = ff[i][j]  # 临时记录，不能直接插入表格
                data = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.tableWidget.setItem(i,j,data)
        # Qt.DescendingOrder 降序
        # Qt.AscendingOrder 升序
        self.tableWidget.sortItems(0, Qt.DescendingOrder)
        #self.tableWidget.itemChanged.connect(self.table_update)
        con.commit()
        con.close()
    def table_save(self):
        from sqlite3 import connect
        db_name = 'source_lines.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('select * from lines')
        #r = cur.fetchall()
        #input_table_rows = len(r)
        #print(len(r))
        
        #input_table_colunms = 11
        #self.tableWidget.setColumnCount(input_table_colunms)
        #self.tableWidget.ColumnCount()
        #self.tableWidget.rowCount()
        
        total_data = []
        for i in range(0,self.tableWidget.rowCount()):
            row_data = []
            for j in range(0, self.tableWidget.columnCount()):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        total_data_2 = np.array(total_data)
        cur.execute('drop table lines')
        cur.execute('create table lines (line_name text,line_mode text, line_area float,line_unit_mass float,line_conductivity float,line_Current_density float,line_Calculation_radius float,line_Equivalent_radius float,line_Dc_resistance float,line_Magnetic_permeability float,line_Relative_permeability float)')
        for item in total_data_2:
            cur.execute('insert into lines(line_name,line_mode,line_area,line_unit_mass,line_conductivity,line_Current_density,line_Calculation_radius,line_Equivalent_radius,line_Dc_resistance,line_Magnetic_permeability,line_Relative_permeability) values(?,?,?,?,?,?,?,?,?,?,?)',item)
        cur.execute('select * from lines')
        con.commit()
        con.close()
   
    def table_insert(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
    def table_delete(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)
        
    

        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    app.exec_()
        
        
