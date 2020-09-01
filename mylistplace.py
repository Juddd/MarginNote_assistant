import sys

from PyQt5.QtWidgets import  QApplication, QDialog
from PyQt5.QtCore import  Qt,QItemSelectionModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QSettings,pyqtSlot

from ui_listplace import Ui_ListReplace
import json
import os

class QmyListPlace(QDialog):
    def __init__(self):
        super().__init__()

        # self.__init_list=[["\n",""],[" ",""],["（","("],["）",")"],[",","，"]]
        self.__init_dic={"\n":{"string":"","used":True}," ":{"string":"","used":True},"（":{"string":"(","used":True},"）":{"string":")","used":True},",":{"string":"，","used":True}}

        if not(os.path.exists("assistant_config.ini")):#配置文件不存在就创建一个
            with open("assistant_config.ini", 'w') as fp:
                json.dump(self.__init_dic, fp, ensure_ascii=False)
        else:#存在就按配置文件的来
            with open("assistant_config.ini", 'r') as fp:
                self.__init_dic = json.load(fp)


        self.ui=Ui_ListReplace()
        self.ui.setupUi(self)

        self.setWindowTitle("配置字符串替换列表")
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.WindowStaysOnTopHint )
        self.itemModel=QStandardItemModel(len(self.__init_dic),3,self)

        self.itemModel.setHorizontalHeaderLabels(["原字符","新字符","是否启用"])
        self.selectionModel = QItemSelectionModel(self.itemModel)

        self.ui.tableView.setModel(self.itemModel)
        self.ui.tableView.setSelectionModel(self.selectionModel)

        self.a=1
        self.__lastColumnTitle = "启用"
        self.__lastColumnFlags = (Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.ui.tableView.setAlternatingRowColors(True)
        self.ui.tableView.setColumnWidth(2,55)

        self.regSettings=QSettings("zyd","Amend_clipboard")
        if not(self.regSettings.contains("chkBox_html")):
            self.regSettings.setValue("chkBox_html",0)
        self.ui.chkBox_html.setChecked(Qt.Checked if self.regSettings.value("chkBox_html")==1 else Qt.Unchecked)



        i=0
        for key,value in self.__init_dic.items():
            old=QStandardItem(key)
            new=QStandardItem(value["string"])
            # if i<2:
            #     old.setEditable(False)
            #     new.setEditable(False)
            self.itemModel.setItem(i,0,old)
            self.itemModel.setItem(i,1,new)

            item = QStandardItem(self.__lastColumnTitle)  # 最后一列
            item.setFlags(self.__lastColumnFlags)
            item.setCheckable(True)
            status=Qt.Checked if value["used"] else Qt.Unchecked
            item.setCheckState(status)

            # item.setTextAlignment(Qt.AlignHCenter)
            self.itemModel.setItem(i,2,item)
            i+=1

        # self.itemModel.item(0,0).setData("这是一个换行符",Qt.ToolTipRole)
        # self.itemModel.item(1,0).setData("这是一个空格",Qt.ToolTipRole)

        #配置全选按扭
        if not(self.regSettings.contains("chk_all")):
            current_status=[v["used"] for k,v in self.__init_dic.items()]
            if all(current_status):#全选
                self.ui.chk_all.setCheckState(Qt.Checked)
                self.regSettings.setValue("chk_all", Qt.Checked)
            else:#没有一个被选
                self.ui.chk_all.setCheckState(Qt.Unchecked)
                self.regSettings.setValue("chk_all", Qt.Unchecked)
        else:
            if self.regSettings.value("chk_all")==Qt.Unchecked:
                self.ui.chk_all.setCheckState(Qt.Unchecked)
            else:
                self.ui.chk_all.setCheckState(Qt.Checked)


    def on_append_row_released(self):
        itemlist = []  # QStandardItem 对象列表
        for i in range(2):  # 不包括最后一列
            item = QStandardItem(str(self.a))
            itemlist.append(item)
        self.a+=1
        item = QStandardItem(self.__lastColumnTitle)  # 最后一列
        item.setCheckable(True)
        item.setFlags(self.__lastColumnFlags)
        item.setCheckState(Qt.Checked)
        itemlist.append(item)

        self.itemModel.appendRow(itemlist)  # 添加一行
        curIndex = self.itemModel.index(self.itemModel.rowCount()-1, 0)
        self.selectionModel.clearSelection()
        self.selectionModel.setCurrentIndex(curIndex, QItemSelectionModel.Select)

    def on_remove_row_released(self):
        curIndex = self.selectionModel.currentIndex()  # 获取当前选择单元格的模型索引
        # if curIndex.row()>1:
        self.itemModel.removeRow(curIndex.row())  # 删除当前行

    @pyqtSlot(bool)
    def on_chkBox_html_clicked(self,qcheck):
        if qcheck:
            self.regSettings.setValue("chkBox_html", 1)
        else:
            self.regSettings.setValue("chkBox_html", 0)

    #chk_all变量中0为全不选，1为部分选,2为全选，
    @pyqtSlot(bool)
    def on_chk_all_clicked(self,qcheck):
        if qcheck:
            self.regSettings.setValue("chk_all", Qt.Checked)
            for i in range(self.itemModel.rowCount()):
                self.itemModel.item(i,2).setCheckState(Qt.Checked)
        else:
            self.regSettings.setValue("chk_all", Qt.Unchecked)
            for i in range(self.itemModel.rowCount()):
                self.itemModel.item(i,2).setCheckState(Qt.Unchecked)


    def getTableContent(self):
        list_replace={}
        for i in range(self.itemModel.rowCount()):
            list_replace[self.itemModel.item(i, 0).text()]={"string":self.itemModel.item(i, 1).text(),"used":self.itemModel.item(i,2).checkState() == Qt.Checked}
        return list_replace


if  __name__ == "__main__":         #用于当前窗体测试
    app = QApplication(sys.argv)    #创建GUI应用程序
    form=QmyListPlace()            #创建窗体
    form.show()
    sys.exit(app.exec_())