import sys

from PyQt5.QtWidgets import  QApplication, QDialog
from PyQt5.QtCore import  Qt,QItemSelectionModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from ui_listplace import Ui_ListReplace


class QmyListPlace(QDialog):
    def __init__(self):
        super().__init__()

        self.__init_list=[["\n",""],[" ",""],["（","("],["）",")"],[",","，"]]
        self.ui=Ui_ListReplace()
        self.ui.setupUi(self)

        self.setWindowTitle("配置字符串替换列表")
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.itemModel=QStandardItemModel(5,3,self)

        self.itemModel.setHorizontalHeaderLabels(["原字符","新字符","是否启用"])
        self.selectionModel = QItemSelectionModel(self.itemModel)

        self.ui.tableView.setModel(self.itemModel)
        self.ui.tableView.setSelectionModel(self.selectionModel)

        self.a=1
        self.__lastColumnTitle = "启用"
        self.__lastColumnFlags = (Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.ui.tableView.setAlternatingRowColors(True)
        self.ui.tableView.setColumnWidth(2,55)

        for i in range(len(self.__init_list)):
            old=QStandardItem(self.__init_list[i][0])
            new=QStandardItem(self.__init_list[i][1])
            if i<2:
                old.setEditable(False)
                new.setEditable(False)
            self.itemModel.setItem(i,0,old)
            self.itemModel.setItem(i,1,new)

            item = QStandardItem(self.__lastColumnTitle)  # 最后一列
            item.setFlags(self.__lastColumnFlags)
            item.setCheckable(True)
            item.setCheckState(Qt.Checked)

            # item.setTextAlignment(Qt.AlignHCenter)
            self.itemModel.setItem(i,2,item)
        self.itemModel.item(0,0).setData("这是一个换行符",Qt.ToolTipRole)
        self.itemModel.item(1,0).setData("这是一个空格",Qt.ToolTipRole)

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
        if curIndex.row()>1:
            self.itemModel.removeRow(curIndex.row())  # 删除当前行

    def getTableContent(self):
        list_replace={}
        for i in range(self.itemModel.rowCount()):
            if self.itemModel.item(i,2).checkState():
                list_replace[self.itemModel.item(i,0).text()]=self.itemModel.item(i,1).text()
        # print(list_replace)
        return list_replace


if  __name__ == "__main__":         #用于当前窗体测试
    app = QApplication(sys.argv)    #创建GUI应用程序
    form=QmyListPlace()            #创建窗体
    form.show()
    sys.exit(app.exec_())