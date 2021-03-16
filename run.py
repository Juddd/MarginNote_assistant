import sys
import statistics
import clipboard as cl
from PyQt5.QtWidgets import QApplication,QSystemTrayIcon,QDialog,QMenu,qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings,pyqtSlot


import json
import imgs_rc
import variable
import re
import time




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
        startupAction.setChecked(self.startup_var.value("Amend_clipboard")==sys.argv[0])
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

        self.last_text=None#上次的内容


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
            # print("进入")
            #剪切板中有文本、没有图片、没有文件列表
            if self.clipboard.mimeData().hasText() and not(self.clipboard.mimeData().hasImage()) and not(self.clipboard.mimeData().hasUrls()) and self.last_text != text:
                #处理编码问题
                processed = "".join([self.re_list_han[x] if x in self.re_list_han else x for x in list(text)])
                comparison = {a: b for a, b in zip(list(text), list(processed)) if a != b}

                #处理英文逗号后面可能带空格的问题，因为英文文章中的","后来是一定会接一个空格的，所以得预处理一下
                if "," in self.re_list:
                    processed = re.sub(", +",",",processed)

                #处理整个对话框列表的问题
                for x in list(processed):
                    if x in self.re_list:
                        result_text+=self.re_list[x]
                        comparison[x]=self.re_list[x]
                    else:
                        result_text+=x
                self.last_text = result_text

                if text != result_text:#字符有替换或编码有调整
                    cl.copy(result_text)

                    n = 0
                    lis=[]
                    while (n < 9):#主要想避免那些无效的“?”
                        cl.copy(result_text)
                        time.sleep(0.05)
                        content = self.clipboard.text()
                        if bool(content):#不为空时记录一下
                            lis.append(content)
                            n += 1
                    print(lis)
                    m = 0
                    while (not (self.clipboard.text()) and m < 10):
                        cl.copy(statistics.mode(lis))
                        time.sleep(0.05)
                        m += 1
                    # print(json.dumps(comparison, ensure_ascii=False).replace(":", "→"))
                    self.showMessage("替换列表：", json.dumps(comparison, ensure_ascii=False).replace(":", "→"))

                elif self.clipboard.mimeData().hasHtml():#什么都没有变但是把html转成了纯文本
                    # print("工作二")
                    cl.copy(text)
                    n = 0
                    while (not (self.clipboard.text()) and n < 10):#这里并不是要求一定要复制10次，只要剪贴板不为空就可以了
                        cl.copy(text)
                        time.sleep(0.05)
                        n += 1
                    self.showMessage("提醒!", "html已转plain")


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
    app.setApplicationVersion("1.27")
    app.setApplicationName("Amend_clipboard")
    app.setOrganizationName("zyd")

    myWidget=MyWidget()
    myWidget.show()
    sys.exit(app.exec_())