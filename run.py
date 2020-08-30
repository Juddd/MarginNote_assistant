import sys
from unicodedata import normalize
import clipboard as cl
from PyQt5.QtWidgets import QApplication,QSystemTrayIcon,QDialog,QMenu,qApp
from PyQt5.QtGui import QIcon

import json
import imgs_rc
import pattern
import re

from mylistplace import QmyListPlace

class MyWidget(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.setIcon(QIcon(":images/img/tray_logo.png"))
        self.setToolTip("修正从MarginNote脑图中复制出来的汉字编码")
        self.showMessage("Message", "Running!")

        menu=QMenu()
        settingAction = menu.addAction("设置")
        settingAction.triggered.connect(self.setting)
        exitAction = menu.addAction("退出")
        exitAction.triggered.connect(self.exit)
        self.setContextMenu(menu)

        self.list_replace_gui=QmyListPlace()

        self.re_list=self.list_replace_gui.getTableContent()

        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.fun)

        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_dialog()

    def fun(self):
        if self.clipboard.mimeData().hasText():
            # print("a:",self.table.item(0,0))
            text = self.clipboard.text()
            tmp = normalize("NFKC", text)

            #处理编码问题
            processed = "".join([pattern.pattern[x] if x in pattern.pattern else x for x in list(tmp)])
            comparison = {a: b for a, b in zip(list(text), list(processed)) if a != b}

            #处理英文逗号后面可能带空格的问题
            if "," in self.re_list:
                processed = re.sub(", +",",",processed)

            #处理整个对话框列表的问题
            result=""
            for x in list(processed):
                if x in self.re_list:
                    result+=self.re_list[x]
                    comparison[x]=self.re_list[x]
                else:
                    result+=x

            # processed = "".join([self.re_list[x] if x in self.re_list else x for x in list(processed)])

            if text != result:
                cl.copy(result)
                # comparison = {a: b for a, b in zip(list(text), list(result)) if a != b}
                self.showMessage("替换列表：", json.dumps(comparison, ensure_ascii=False))
            # print(text)
            # print(new_tex)


    def setting(self):
        self.show_dialog()


    def show_dialog(self):
        status = self.list_replace_gui.exec()
        if status == QDialog.Accepted:
            self.re_list=self.list_replace_gui.getTableContent()
        # print(self.re_list)


    def exit(self):
        qApp.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    myWidget=MyWidget()
    myWidget.show()
    sys.exit(app.exec_())