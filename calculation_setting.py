# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QPushButton

from Ui_calculation_setting import Ui_Dialog


class set_cal(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self,fileName, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(set_cal, self).__init__(parent)
        self.fileName = fileName
        self.setupUi(self)
        self.setWindowTitle("计算参数设置")
        self.comboBox.addItems(["请选择","10", "6", "4"])
        self.checkBox.clicked.connect(self.locomotive)
        self.pushButton_5.clicked.connect(self.table_insert)
        self.pushButton_6.clicked.connect(self.table_delete)
        self.pushButton_7.clicked.connect(self.set_save)
        
    def locomotive(self):
        self.tableWidget.clear()###清空上一个表格的数据
        input_table_rows = 4
        input_table_header = ['属性','机车1', '机车2', '机车3', '机车4']
        input_table_colunms = len(input_table_header)##9列
        self.tableWidget.setColumnCount(input_table_colunms)
        self.tableWidget.setHorizontalHeaderLabels(input_table_header)
        self.tableWidget.setRowCount(input_table_rows)
        self.tableWidget.verticalHeader().setVisible(False)#隐藏垂直表头
        line_name =  ['位置(Km)','取流(A)','上下行（1为上行，0为下行）','1']
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
            for j in range(2, 5):
                    temp_data = line_name_f[i]  # 临时记录，不能直接插入表格
                    data = QTableWidgetItem(temp_data)  # 转换后可插入表格
                    self.tableWidget.setItem(i, j, data)         
    def table_insert(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        item_1 = QTableWidgetItem("0")###可替换为老师程序中的初始值
        item_2 = QTableWidgetItem("0")###可替换为老师程序中的初始值
        item_3 = QTableWidgetItem("0")###可替换为老师程序中的初始值
        item_4 = QTableWidgetItem("0")###可替换为老师程序中的初始值
        
        self.tableWidget.setItem(row, 1, item_1)
        self.tableWidget.setItem(row, 2, item_2)
        self.tableWidget.setItem(row, 3, item_3)
        self.tableWidget.setItem(row, 4, item_4)
    def table_delete(self):
        row_select = self.tableWidget.selectedItems()
        if len(row_select) == 0:
            return
        id = row_select[0].text()
        print("id: {}".format(id))
 
        row = row_select[0].row()
        self.tableWidget.removeRow(row)        
    def set_save(self):
        total_data = []
        for i in range(self.tableWidget.rowCount()):
            row_data = [] 
            for j in range(self.tableWidget.columnCount()):
                row_data.append(self.tableWidget.item(i, j).text())
            total_data.append(row_data)
        from sqlite3 import connect
        con1 = connect(self.fileName)# 取得数据库连接对象
        cur1 = con1.cursor()  # 取得数据库游标对象
        cur1.execute('drop table if exists locomotive')  # 解决提��star已存在的问题
        #cur.execute('drop table if exists base_set')  # 解决提��star已存在的问题
        cur1.execute('create table locomotive(name_locomotive text,locomotive1 float,locomotive2 float,locomotive3 float,locomotive4 float)')
        #cur.execute('create table base_setting(chain_model float,block_length text)')
        for item in total_data:
            cur1.execute('insert into locomotive(name_locomotive,locomotive1,locomotive2,locomotive3,locomotive4) values(?,?,?,?,?)',item)
        cur1.execute('select * from locomotive')
        for row in cur1:
                print(row)

        con1.commit()
        con1.close()
        con2 = connect(self.fileName)  # 取得数据库连接对象
        cur2 = con2.cursor()  # 取得数据库游标对象
        block_length = self.lineEdit.text()
        chain_model = self.comboBox.currentText()
        cur2.execute('update base set block_length=?', (block_length, ))
        cur2.execute('update base set chain_model=?', (chain_model, ))
        con2.commit()
        con2.close()




















