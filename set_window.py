# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5.QtWidgets import QDialog, QApplication

from Ui_set_window import Ui_Dialog

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
        self.setWindowTitle("AT牵引供电系统")
        self.pushButton_1.clicked.connect(self.set_para)
        self.pushButton_2.clicked.connect(self.set_save)
    
    def set_save(self):
        Length = self.lineEdit_1.text()   #供电臂长度
        delta_length = self.lineEdit_2.text()   #分段长度
        rou = self.lineEdit_3.text()   #大地导电率
        total_data =[ [Length, delta_length, rou]]
        print(total_data)
        from sqlite3 import connect
        db_name = 'test_calculate.db'
        con = connect(db_name)  # 取得数据库连接对象
        cur = con.cursor()  # 取得数据库游标对象
        cur.execute('drop table if exists star_topo')  # 解决提��star已存在的问题
        cur.execute('create table star_topo(Length float,delta_length float,rou float)')
        for item in total_data:
            print(item)
        for item in total_data:
            cur.execute('insert into star_topo(Length,delta_length,rou) values(?,?,?)',item)
        cur.execute('select * from star_topo')
        for row in cur:
                print(row)
        con.commit()
        con.close()      
        
         
        
        
        
        
        

    def set_para(self):
        from topology import Dialog
        d = Dialog()
        d.exec_()    
        
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Dialog()
    form.show()
    app.exec_()  
