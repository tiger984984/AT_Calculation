from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox
#from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from sqlite3 import connect
import os

class TableDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()
        
    def createEditor(self, parent, option, index):
         #连接数据库，取出导线类型
        os.chdir("../data")
        data_source = 'line_source.db'
        con = connect(data_source)
        cursor = con.cursor()
        com = cursor.execute('select type_name from lines_source')
        #从lines_source表中取出导线类型
        lines_list = []
        alllines = com.fetchall()
        for l in alllines:
            lines_list.append(l[0])
        #将取出的导线型号名称变为List
        
        
       
        
         #取出钢轨的型号变为List
        com = cursor.execute('select type_name from rail_source')
        rail_list = []
        allrail = com.fetchall()
        for r in allrail:
            rail_list.append(r[0])
        #print(rail_list)
        
        #为导线和钢轨加入型号选择下拉框，
        editor = QComboBox(parent)
        
        if index.column() == 2 and index.row() in [0, 1, 2, 5, 6, 7, 8, 9, 12, 13]:
            editor.addItems(lines_list)
            return editor
            #导线
        elif index.column() == 2 and index.row() in [3, 4, 10, 11]:
            editor.addItems(rail_list)
            return editor
            #钢轨
        else:
            return super().createEditor(parent, option, index)
         
        con.close()
        
    def setModelData(self, editor, model, index):
        if index.column() == 0:
            strData = editor.currentText()
            model.setData(index, strData, Qt.EditRole)
        else:
            return super().setModelData(editor, model, index)
            
