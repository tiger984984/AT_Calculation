# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from Ui_show_results import Ui_Dialog
import matplotlib.pyplot as plt
#from Ui_tractionpower_interface import Ui_MainWindow
#from tractionpower_interface import MainWindow
class results(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self,fileName, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(results, self).__init__(parent)
        self.fileName = fileName
        self.setupUi(self)
        self.setWindowTitle("牵引供电系统特性计算")
        #计算正常运行情况下的电压电流
        self.pushButton_3.clicked.connect(self.set_ui_m)
        #计算各导线短路阻抗曲线
        self.pushButton_4.clicked.connect(self.set_short_circuit_m)
        #设置导线类型
        self.set_number_ui()
        self.set_number_z()
        self.comboBox_1.currentIndexChanged.connect(self.select_ui)
        self.comboBox_2.currentIndexChanged.connect(self.select_z)
        
    def select_ui(self):
        #输入合并后的数目
        from sqlite3 import connect
        con = connect(self.fileName)# 取得数据库连接对象
        cur_chain_model = con.cursor()  # 取得数据库游标对象
        #cur_chain_model.execute('drop table if exists ?', (self.fileName, ))  # 解决提示star已存在的问题
        cur_chain_model.execute('select chain_model from base')
        for row_chain_model in cur_chain_model:
                print(row_chain_model)
        con.commit()
        #con.close()
        print(type(row_chain_model))
        #print(str(row))
        #print(type(str(row)))
        chain_model_set = list(row_chain_model)[0]
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        print(chain_model_set)
       #输入分段长度
        from sqlite3 import connect
        con = connect(self.fileName)# 取得数据库连接对象
        cur_block_length = con.cursor()  # 取得数据库游标对象
        #cur_block_length.execute('drop table if exists fileName')  # 解决提示star已存在的问题
        cur_block_length.execute('select block_length from base')
        for row_block_length in cur_block_length:
                print(row_block_length)
        con.commit()
        con.close()
        block_length_set = list(row_block_length)[0]
        import numpy as np
        from scipy import linalg
        import Ipynb_importer
        import new_topology as tp
        import conductor_calculation as cc
        import calculation as ca
        chen = ca.ChainNetwork()
        print("测试mmmmmmmmmmmmmmmmmmm")
        print(self.fileName)
        chen.reset(1,int(chain_model_set),float(block_length_set), self.fileName)
        chen.set_z_y()
        if chen.m == 6 or chen.m == 10:
            chen.add_y_AT()
        YY = chen.add_y_source()
        chen.add_y()
        R = chen.source()
        chen.locomotives()
        U, I = chen.solution()
        line_model=self.comboBox_1.currentText()
        p = 0               ###缺省值
        if chen.m == 6:
            if line_model == "上行接触线":
                p = 0
            elif line_model == "上行馈线":
                p = 1
            elif line_model == "上行钢轨":
                p = 2
            elif line_model == "下行接触线":
                p = 3
            elif line_model == "下行馈线":
                p = 4
            elif line_model == "下行钢轨":
                p = 5
        elif chen.m == 4:
            if line_model == "上行接触线":
                p = 0
            elif line_model == "上行钢轨":
                p = 1
            elif line_model == "下行接触线":
                p = 2
            elif line_model == "下行钢轨":
                p = 3
        elif chen.m == 10:
            if line_model == "上行接触线":
                p = 0
            elif line_model == "上行馈线":
                p = 1
            elif line_model == "上行钢轨":
                p = 2
            elif line_model == "上行保护线":
                p = 3
            elif line_model == "上行综合地线":
                p = 4
            elif line_model == "下行接触线":
                p = 5
            elif line_model == "下行馈线":
                p = 6
            elif line_model == "下行钢轨":
                p = 7
            elif line_model == "下行保护线":
                p = 8
            elif line_model == "下行综合地线":
                p = 9
        elif chen.m == 4:
            if line_model == "上行接触线":
                p = 0
            elif line_model == "上行钢轨":
                p = 1
            elif line_model == "下行接触线":
                p = 2
            elif line_model == "下行钢轨":
                p = 3
        #绘制某次谐波下的电流特性曲线
        Distances = chen.distances
        ####取模值###########################
        simple_U = np.zeros((U.shape[0], U.shape[1]), np.float64)
        simple_I = np.zeros((I.shape[0], I.shape[1]), np.float64)
        for k in range(U.shape[0]):
            for j in range(U.shape[1]):
                simple_U[k][j] = abs(U[k][j])
        for k in range(I.shape[0]):
            for j in range(I.shape[1]):
                simple_I[k][j] = abs(I[k][j])
        
        
        from matplotlib.font_manager import FontProperties
        font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
        plt.figure()
        plt.suptitle(u'正常运行情况下导线电压电流曲线',fontsize=10,fontproperties=font_set)
        plt.subplot(2, 2, 1)
        plt.plot(Distances[:-1].tolist(), simple_I[p][:].tolist(), color='red')
        plt.title(u'' + chen.topology.lines_system + '工频下'+ line_model +'电流特性曲线', fontproperties=font_set)
        plt.xlabel(u'距离x/Km', fontproperties=font_set)
        plt.ylabel(u'电流i/A', fontproperties=font_set)
        plt.show()
        #plt.figure()
        plt.subplot(2, 2, 2)
        plt.plot(Distances.tolist(), simple_U[p][:].tolist(), color='red')
        plt.title(u'' + chen.topology.lines_system + '工频下' + line_model +'电压特性曲线', fontproperties=font_set)
        plt.xlabel(u'距离x/Km', fontproperties=font_set)
        plt.ylabel(u'电压u/V', fontproperties=font_set)
        plt.show() 
        #电压电流不同合并方式
    def set_number_ui(self):
        #输入合并后的数目
        from sqlite3 import connect
        #os.chdir('../user')
        con = connect(self.fileName)# 取得数据库连接对象
        cur_chain_model = con.cursor()  # 取得数据库游标对象
        #cur_chain_model.execute('drop table if exists calculate_system')  # 解决提示star已存在的问题
        cur_chain_model.execute('select chain_model from base')
        for row_chain_model in cur_chain_model:
                print(row_chain_model)
        con.commit()
        con.close()
        print(type(row_chain_model))
        chain_model_set = list(row_chain_model)[0]
        print(chain_model_set)
        if chain_model_set == 6:
            self.comboBox_1.addItems(["请选择","上行接触线", "上行馈线", "上行钢轨","下行接触线","下行馈线","下行钢轨"])
        elif chain_model_set ==10:
            self.comboBox_1.addItems(["请选择","上行接触线", "上行钢轨", "上行馈线", "上行保护线", "上行综合地线", "下行接触线", "下行钢轨", "下行馈线", "下行保护线", "下行综合地线"])
        else:
            self.comboBox_1.addItems(["请选择","上行接触线", "上行钢轨", "下行接触线", "下行钢轨"])
    def set_number_z(self):
        #输入合并后的数目
        from sqlite3 import connect
        con = connect(self.fileName)# 取得数据库连接对象
        cur_chain_model = con.cursor()  # 取得数据库游标对象
        #cur_chain_model.execute('drop table if exists calculate_system')  # 解决提示star已存在的问题
        cur_chain_model.execute('select chain_model from base')
        for row_chain_model in cur_chain_model:
                print(row_chain_model)
        con.commit()
        con.close()
        print(type(row_chain_model))
        chain_model_set = list(row_chain_model)[0]
        print(chain_model_set)
        if chain_model_set == 6:
            self.comboBox_2.addItems(["请选择","上行接触线T1-上行钢轨R1", "上行接触线T1-上行馈线PF1"])
        elif chain_model_set ==10:
            self.comboBox_2.addItems(["请选择","上行接触线T1-上行钢轨R1", "上行接触线T1-上行馈线PF1"])
        else:
            self.comboBox_2.addItems(["请选择","上行接触线T1-上行钢轨R1"])
    
 
    
    #计算正常运行情况下电压电流
    def set_ui_m(self):
        #输入合并后的数目和分段长度
        from sqlite3 import connect
        con = connect(self.fileName)# 取得数据库连接对象
        cur_chain_model = con.cursor()  # 取得数据库游标对象
        cur_block_length = con.cursor()  # 取得数据库游标对象
        #cur_chain_model.execute('drop table if exists calculate_system')  # 解决提示star已存在的问题
        cur_chain_model.execute('select chain_model from base')
        cur_block_length.execute('select block_length from base')
        for row_block_length in cur_block_length:
                print(row_block_length)
        for row_chain_model in cur_chain_model:
                print(row_chain_model)
        con.commit()
        con.close()
        print(type(row_chain_model))
        chain_model_set = list(row_chain_model)[0]
        block_length_set = list(row_block_length)[0]
        
        #计算电压和电流
        import numpy as np
        from scipy import linalg
        import Ipynb_importer
        
        import new_topology as tp
        import conductor_calculation as cc
        import calculation as ca
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        chen = ca.ChainNetwork()
        chen.reset(1,int(chain_model_set),float(block_length_set), self.fileName)
        #print(int(chain_model_set),float(block_length_set), db_name)
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        chen.set_z_y()
        if chen.m == 6 or chen.m == 10:
            chen.add_y_AT()
        YY = chen.add_y_source()
        chen.add_y()
        R = chen.source()
        chen.locomotives()
        U, I = chen.solution()
        print("fsfsfsfffffffffffffffffffffffffffffffffffffffffffffffffff")
        print(U)
        
        
        Distances = chen.distances
        simple_U = np.zeros((U.shape[0], U.shape[1]), np.float64)
        simple_I = np.zeros((I.shape[0], I.shape[1]), np.float64)
        for k in range(simple_U.shape[0]):
            for j in range(simple_U.shape[1]):
                simple_U[k][j] = abs(U[k][j])
        for k in range(I.shape[0]):
            for j in range(I.shape[1]):
                simple_I[k][j] = abs(I[k][j])
        
        if chen.m == 6:
            #input_table_header = ['上行接触线', '上行馈线', '上行钢轨','下行接触线','下行馈线','下行钢轨']
            #for p in range(6):
            from matplotlib.font_manager import FontProperties
            font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
            plt.figure()
            plt.suptitle(u'正常运行情况下各导线电压曲线',fontsize=30,fontproperties=font_set )
            plt.subplot(3, 2, 1)
            plt.plot(Distances.tolist(), simple_U[0][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行接触线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(3, 2, 2)
            plt.plot(Distances.tolist(), simple_U[1][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行馈线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(3, 2, 3)
            plt.plot(Distances.tolist(), simple_U[2][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行钢轨' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(3, 2, 4)
            plt.plot(Distances.tolist(), simple_U[3][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行接触线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(3, 2, 5)
            plt.plot(Distances.tolist(), simple_U[4][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行馈线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(3, 2, 6)
            plt.plot(Distances.tolist(), simple_U[5][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行钢轨' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()

            plt.figure()
            plt.suptitle(u'正常运行情况下牵引网各导线电流曲线',fontsize=30,fontproperties=font_set)
            plt.subplot(3, 2, 1)
            plt.plot(Distances[:-1].tolist(), simple_I[0][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下'+ '上行接触线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电流i/A', fontproperties=font_set)
            plt.show()  
            plt.subplot(3, 2, 2)
            plt.plot(Distances[:-1].tolist(), simple_I[1][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下'+ '上行馈线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电流i/A', fontproperties=font_set)
            plt.show()            
            plt.subplot(3, 2, 3)
            plt.plot(Distances[:-1].tolist(), simple_I[2][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下'+ '上行钢轨' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电流i/A', fontproperties=font_set)
            plt.show()            
            plt.subplot(3, 2, 4)
            plt.plot(Distances[:-1].tolist(), simple_I[3][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下'+ '下行接触线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电流i/A', fontproperties=font_set)
            plt.show()
            plt.subplot(3, 2, 5)
            plt.plot(Distances[:-1].tolist(), simple_I[4][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下'+ '下行馈线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电流i/A', fontproperties=font_set)
            plt.show()            
            plt.subplot(3, 2, 6)
            plt.plot(Distances[:-1].tolist(), simple_I[5][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下'+ '下行钢轨' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电流i/A', fontproperties=font_set)
            plt.show()
            
            
        elif chen.m == 4:
            from matplotlib.font_manager import FontProperties
            font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
            plt.figure()
            plt.suptitle(u'正常运行情况下牵引网各导线电压曲线',fontsize=30,fontproperties=font_set)
            plt.subplot(2, 2, 1)
            plt.plot(Distances.tolist(), simple_U[0][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行接触线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(2, 2, 2)
            plt.plot(Distances.tolist(), simple_U[1][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行钢轨' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(2, 2, 3)
            plt.plot(Distances.tolist(), simple_U[2][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行接触线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(2, 2, 4)
            plt.plot(Distances.tolist(), simple_U[3][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行钢轨' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()

            plt.figure()
            plt.suptitle(u'正常运行情况下牵引网各导线电流曲线',fontsize=30,fontproperties=font_set)
            plt.subplot(2, 2, 1)
            plt.plot(Distances[:-1].tolist(), simple_I[0][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下'+ '上行接触线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电流i/A', fontproperties=font_set)
            plt.show()  
            plt.subplot(2, 2, 2)
            plt.plot(Distances[:-1].tolist(), simple_I[1][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下'+ '上行馈线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电流i/A', fontproperties=font_set)
            plt.show()            
            plt.subplot(2, 2, 3)
            plt.plot(Distances[:-1].tolist(), simple_I[2][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下'+ '下行接触线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电流i/A', fontproperties=font_set)
            plt.show()
            plt.subplot(3, 2, 4)
            plt.plot(Distances[:-1].tolist(), simple_I[3][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下'+ '下行钢轨' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电流i/A', fontproperties=font_set)
            plt.show()
            
        elif chen.m == 10:
            from matplotlib.font_manager import FontProperties
            font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
            plt.figure()
            plt.suptitle(u'正常运行情况下牵引网各导线电压曲线',fontsize=30,fontproperties=font_set)
            plt.subplot(5, 2, 1)
            plt.plot(Distances.tolist(), simple_U[0][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行接触线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 2)
            plt.plot(Distances.tolist(), simple_U[1][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行馈线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 3)
            plt.plot(Distances.tolist(), simple_U[2][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行钢轨' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 4)
            plt.plot(Distances.tolist(), simple_U[3][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行保护线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 5)
            plt.plot(Distances.tolist(), simple_U[4][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行综合底线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 6)
            plt.plot(Distances.tolist(), simple_U[5][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行接触线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 7)
            plt.plot(Distances.tolist(), simple_U[6][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行馈线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 8)
            plt.plot(Distances.tolist(), simple_U[7][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行钢轨' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 9)
            plt.plot(Distances.tolist(), simple_U[8][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行保护线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 10)
            plt.plot(Distances.tolist(), simple_U[9][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行综合底线' +'电压特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            
            plt.figure()
            plt.suptitle(u'正常运行情况下牵引网各导线电流曲线',fontsize=30,fontproperties=font_set)
            plt.subplot(5, 2, 1)
            plt.plot(Distances[:-1].tolist(), simple_I[0][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行接触线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 2)
            plt.plot(Distances[:-1].tolist(), simple_I[1][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行馈线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 3)
            plt.plot(Distances[:-1].tolist(), simple_I[2][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行钢轨' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 4)
            plt.plot(Distances[:-1].tolist(), simple_I[3][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行保护线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 5)
            plt.plot(Distances[:-1].tolist(), simple_I[4][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '上行综合底线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 6)
            plt.plot(Distances[:-1].tolist(), simple_I[5][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行接触线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 7)
            plt.plot(Distances[:-1].tolist(), simple_I[6][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行馈线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 8)
            plt.plot(Distances[:-1].tolist(), simple_I[7][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行钢轨' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 9)
            plt.plot(Distances[:-1].tolist(), simple_I[8][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行保护线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
            plt.subplot(5, 2, 10)
            plt.plot(Distances[:-1].tolist(), simple_I[9][:].tolist(), color='red')
            plt.title(u'' + chen.topology.lines_system + '工频下' + '下行综合底线' +'电流特性曲线', fontproperties=font_set)
            plt.xlabel(u'距离x/Km', fontproperties=font_set)
            plt.ylabel(u'电压u/V', fontproperties=font_set)
            plt.show()
    #计算各导线短路阻抗曲线（所有）
    def set_short_circuit_m(self):
        print("成功")
        from sqlite3 import connect
        con = connect(self.fileName)# 取得数据库连接对象
        cur_chain_model = con.cursor()  # 取得数据库游标对象
        cur_block_length = con.cursor()  # 取得数据库游标对象
        #cur_chain_model.execute('drop table if exists calculate_system')  # 解决提示star已存在的问题
        cur_chain_model.execute('select chain_model from base')
        cur_block_length.execute('select block_length from base')
        for row_block_length in cur_block_length:
                print(row_block_length)
        for row_chain_model in cur_chain_model:
                print(row_chain_model)
        con.commit()
        con.close()
        print(type(row_chain_model))
        chain_model_set = list(row_chain_model)[0]
        block_length_set = list(row_block_length)[0]
        if  int(chain_model_set) == 6:
            import numpy as np
            from scipy import linalg
            import Ipynb_importer
            import new_topology as tp
            import conductor_calculation as cc
            import calculation as ca
            import short_circuit as aa
            chen2 = aa.ChainNetwork_shortc_circuit()
            chen2.reset(int(chain_model_set), float(block_length_set), self.fileName)
            from matplotlib.font_manager import FontProperties
            font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
            plt.figure()
            plt.suptitle(u'牵引网短路阻抗曲线',fontsize=20,fontproperties=font_set)
            plt.subplot(2, 2, 1)
            chen2.plotting_short_circuit_curve(series_mode="上行接触线T1-上行钢轨R1")
            plt.subplot(2, 2, 2)
            chen2.plotting_short_circuit_curve(series_mode="上行接触线T1-上行馈线PF1")
            #可以继续添加其他类型短路阻抗曲线
            print("成功成功！")
        elif  int(chain_model_set) == 10:
            import numpy as np
            from scipy import linalg
            import Ipynb_importer
            import new_topology as tp
            import conductor_calculation as cc
            import calculation as ca
            import short_circuit as aa
            chen2 = aa.ChainNetwork_shortc_circuit()
            chen2.reset(int(chain_model_set), float(block_length_set), self.fileName)
            from matplotlib.font_manager import FontProperties
            font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
            plt.figure()
            plt.suptitle(u'牵引网短路阻抗曲线',fontsize=20,fontproperties=font_set)
            plt.subplot(2, 2, 1)
            chen2.plotting_short_circuit_curve(series_mode="上行接触线T1-上行钢轨R1")
            plt.subplot(2, 2, 2)
            chen2.plotting_short_circuit_curve(series_mode="上行接触线T1-上行馈线PF1")
            #可以继续添加其他类型短路阻抗曲线
            print("成功成功！")
        elif  int(chain_model_set) == 4:
            import numpy as np
            from scipy import linalg
            import Ipynb_importer
            import new_topology as tp
            import conductor_calculation as cc
            import calculation as ca
            import short_circuit as aa
            chen2 = aa.ChainNetwork_shortc_circuit()
            chen2.reset(int(chain_model_set), float(block_length_set), self.fileName)
            from matplotlib.font_manager import FontProperties
            font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
            plt.figure()
            plt.suptitle(u'牵引网短路阻抗曲线',fontsize=20,fontproperties=font_set)
            plt.subplot(1, 1, 1)
            chen2.plotting_short_circuit_curve(series_mode="上行接触线T1-上行钢轨R1")
            #可以继续添加其他类型短路阻抗曲线
            print("成功成功！")
    def select_z(self):
            from sqlite3 import connect
            con = connect(self.fileName)# 取得数据库连接对象
            cur_chain_model = con.cursor()  # 取得数据库游标对象
            cur_block_length = con.cursor()  # 取得数据库游标对象
            #cur_chain_model.execute('drop table if exists calculate_system')  # 解决提示star已存在的问题
            cur_chain_model.execute('select chain_model from base')
            cur_block_length.execute('select block_length from base')
            for row_block_length in cur_block_length:
                    print(row_block_length)
            for row_chain_model in cur_chain_model:
                    print(row_chain_model)
            con.commit()
            con.close()
            print(type(row_chain_model))
            chain_model_set = list(row_chain_model)[0]
            block_length_set = list(row_block_length)[0]
            import numpy as np
            from scipy import linalg
            import Ipynb_importer
            import new_topology as tp
            import conductor_calculation as cc
            import calculation as ca
            import short_circuit as aa
            chen2 = aa.ChainNetwork_shortc_circuit()
            chen2.reset(int(chain_model_set), float(block_length_set),self.fileName)
           # from matplotlib.font_manager import FontProperties
            #font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
            plt.figure()
            #plt.suptitle(u'牵引网短路阻抗曲线',fontsize=30,fontproperties=font_set)
            plt.subplot(1, 1, 1)
            print("成功成功成功")
            print(self.comboBox_2.currentText())
            chen2.plotting_short_circuit_curve(series_mode=self.comboBox_2.currentText())
            #chen2.plotting_short_circuit_curve(self.comboBox_2.currentText())
            #可以继续添加其他类型短路阻抗曲线
            print("成功成功！")
        
        
        

#if __name__ == '__main__':
    #import sys
    #app = QApplication(sys.argv)
    #form = results()
    #form.show()
    #app.exec_()  

