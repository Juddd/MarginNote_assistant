# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\listreplace.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ListReplace(object):
    def setupUi(self, ListReplace):
        ListReplace.setObjectName("ListReplace")
        ListReplace.resize(330, 398)
        self.tableView = QtWidgets.QTableView(ListReplace)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 311, 261))
        self.tableView.setObjectName("tableView")
        self.layoutWidget = QtWidgets.QWidget(ListReplace)
        self.layoutWidget.setGeometry(QtCore.QRect(180, 360, 141, 35))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnok = QtWidgets.QPushButton(self.layoutWidget)
        self.btnok.setObjectName("btnok")
        self.horizontalLayout.addWidget(self.btnok)
        self.btncancel = QtWidgets.QPushButton(self.layoutWidget)
        self.btncancel.setObjectName("btncancel")
        self.horizontalLayout.addWidget(self.btncancel)
        self.frame = QtWidgets.QFrame(ListReplace)
        self.frame.setGeometry(QtCore.QRect(10, 310, 311, 41))
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.chkBox_html = QtWidgets.QCheckBox(self.frame)
        self.chkBox_html.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.chkBox_html.setObjectName("chkBox_html")
        self.widget = QtWidgets.QWidget(ListReplace)
        self.widget.setGeometry(QtCore.QRect(20, 280, 55, 18))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.append_row = QtWidgets.QPushButton(self.widget)
        self.append_row.setStyleSheet("border:0px")
        self.append_row.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/img/plus_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.append_row.setIcon(icon)
        self.append_row.setIconSize(QtCore.QSize(16, 16))
        self.append_row.setObjectName("append_row")
        self.horizontalLayout_2.addWidget(self.append_row)
        self.remove_row = QtWidgets.QPushButton(self.widget)
        self.remove_row.setStyleSheet("border:0px")
        self.remove_row.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/img/minus_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.remove_row.setIcon(icon1)
        self.remove_row.setIconSize(QtCore.QSize(23, 16))
        self.remove_row.setObjectName("remove_row")
        self.horizontalLayout_2.addWidget(self.remove_row)

        self.retranslateUi(ListReplace)
        self.btnok.clicked.connect(ListReplace.accept)
        self.btncancel.clicked.connect(ListReplace.reject)
        QtCore.QMetaObject.connectSlotsByName(ListReplace)

    def retranslateUi(self, ListReplace):
        _translate = QtCore.QCoreApplication.translate
        ListReplace.setWindowTitle(_translate("ListReplace", "ListReplace"))
        self.btnok.setText(_translate("ListReplace", "确认"))
        self.btncancel.setText(_translate("ListReplace", "取消"))
        self.chkBox_html.setText(_translate("ListReplace", "html转plain"))
        self.append_row.setToolTip(_translate("ListReplace", "<html><head/><body><p>添加一行</p></body></html>"))
        self.append_row.setWhatsThis(_translate("ListReplace", "<html><head/><body><p><br/></p></body></html>"))
        self.remove_row.setToolTip(_translate("ListReplace", "<html><head/><body><p>删除本行</p></body></html>"))
import imgs_rc
