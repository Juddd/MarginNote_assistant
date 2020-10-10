import sys
from unicodedata import normalize
import clipboard as cl
from PyQt5.QtWidgets import QApplication,QSystemTrayIcon,QDialog,QMenu,qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings,pyqtSlot


import json
import imgs_rc
import variable
import re

import win32clipboard as wc
import win32con


def get_text():
    """ 读取 """
    wc.OpenClipboard()
    text = wc.GetClipboardData()
    wc.CloseClipboard()
    return text


def set_text(strs):
    """ 写入 """
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardData(strs)


from mylistplace import QmyListPlace


class MyWidget(QSystemTrayIcon):
    #注册表中un_valid为0则停用全局禁止，为1则启用
    def __init__(self):
        super().__init__()

        self.re_list_han=variable.radicals
        self.re_list_han.update(variable.supplement)
        # self.punctuation=set("，、？：！（）")

        self.regSettings=QSettings("zyd","Amend_clipboard")
        if not(self.regSettings.contains("un_valid")):
            self.regSettings.setValue("un_valid",0)

        self.setIcon(QIcon(":images/img/tray_logo.png"))
        self.setToolTip("修正从MarginNote脑图中复制出来的汉字编码")
        self.showMessage("Message", "Running!")

        menu=QMenu()
        #开机自启按扭
        #配置开机自启注册表路径
        self.startup_var=QSettings(variable.RUN_PATH, QSettings.NativeFormat)
        # if self.startup_var.value("Amend_clipboard")!=sys.argv[0]:
        #     self.startup_var.setValue("Amend_clipboard",sys.argv[0])

        startupAction=menu.addAction("开机自启")


        startupAction.setCheckable(True)
        startupAction.setChecked(self.startup_var.contains("Amend_clipboard"))
        startupAction.triggered.connect(self.app_startup)
        menu.addSeparator()
        #设置是否禁用剪贴板监控
        # self.un_valid=False
        validAction=menu.addAction("全局禁用")
        validAction.setCheckable(True)
        validAction.setChecked(self.regSettings.value("un_valid")==1)
        validAction.triggered.connect(self.set_valid)
        menu.addSeparator()
        #设置和退出
        settingAction = menu.addAction("设置")
        settingAction.triggered.connect(self.setting)
        exitAction = menu.addAction("退出")
        exitAction.triggered.connect(self.exit)
        self.setContextMenu(menu)

        self.list_replace_gui=QmyListPlace()

        self.re_dic=self.list_replace_gui.getTableContent()
        # with open("assistant_config.ini", 'w') as fp:
        #     json.dump(self.re_dic, fp, ensure_ascii=False)

        #来源于对话框的替换列表
        self.re_list={k:v["string"] for k,v in self.re_dic.items() if v["used"]}


        self.clipboard = QApplication.clipboard()

        self.last_text=None


        self.clipboard.dataChanged.connect(self.fun)
        #关联双击托盘动作
        self.activated.connect(self.onTrayIconActivated)

    @pyqtSlot(bool)
    def set_valid(self,qvalid):
        if qvalid:#打勾
            self.regSettings.setValue("un_valid", 1)
        else:#没打勾
            self.regSettings.setValue("un_valid", 0)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.setting()

    @pyqtSlot(bool)
    def app_startup(self,qstart):
        if qstart:
            self.startup_var.setValue("Amend_clipboard",sys.argv[0])
        else:
            self.startup_var.remove("Amend_clipboard")

    def fun(self):
        if self.regSettings.value("un_valid")==0:
            text = self.clipboard.text()
            result_text = ""
            # variable.radicals.update(variable)
            if self.clipboard.mimeData().hasText() and not(self.clipboard.mimeData().hasImage()) and self.last_text != text:
                #处理编码问题
                processed = "".join([self.re_list_han[x] if x in self.re_list_han else x for x in list(text)])
                comparison = {a: b for a, b in zip(list(text), list(processed)) if a != b}

                #处理英文逗号后面可能带空格的问题
                if "," in self.re_list:
                    processed = re.sub(", +",",",processed)

                # print("self.re_list:",self.re_list)
                #处理整个对话框列表的问题
                for x in list(processed):
                    if x in self.re_list:
                        result_text+=self.re_list[x]
                        comparison[x]=self.re_list[x]
                    else:
                        result_text+=x
                self.last_text = result_text

                # print("cc")
                if text != result_text:
                    cl.copy(result_text)
                    self.showMessage("替换列表：", json.dumps(comparison, ensure_ascii=False))

                # print(text)
                # print(new_tex)
            if self.regSettings.value("chkBox_html")==1 and not(self.clipboard.mimeData().hasImage()) and self.clipboard.mimeData().hasHtml() and text == self.last_text:
            # if self.regSettings.value("chkBox_html")==1 and not(self.clipboard.mimeData().hasImage()) and self.clipboard.mimeData().hasHtml():
                cl.copy(text)
                n=0
                while(not(self.clipboard.text()) and n < 10):
                    cl.copy(text)
                    n+=1

                self.showMessage("提醒!","html已转plain")


    def setting(self):
        self.list_replace_gui=QmyListPlace()
        self.re_dic=self.list_replace_gui.getTableContent()
        self.re_list={k:v["string"] for k,v in self.re_dic.items() if v["used"]}

        status = self.list_replace_gui.exec()
        if status == QDialog.Accepted:
            self.re_dic = self.list_replace_gui.getTableContent()
            with open("assistant_config.ini", 'w') as fp:
                json.dump(self.re_dic, fp, ensure_ascii=False)

            self.re_list = {k: v["string"] for k, v in self.re_dic.items() if v["used"]}
        # print(self.re_list)


    def exit(self):
        qApp.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationVersion("1.19")
    app.setApplicationName("Amend_clipboard")
    app.setOrganizationName("zyd")

    myWidget=MyWidget()
    myWidget.show()
    sys.exit(app.exec_())