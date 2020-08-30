import sys
from unicodedata import normalize
import clipboard as cl
from PyQt5.QtWidgets import QApplication,QSystemTrayIcon,QDialog,QMenu,qApp,QWidget
from PyQt5.QtGui import QIcon

import json
import imgs_rc
import pattern

from mylistplace import QmyListPlace

class MyWidget(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        menu=QMenu()
        settingAction = menu.addAction("设置")
        settingAction.triggered.connect(self.setting)
        exitAction = menu.addAction("退出")
        exitAction.triggered.connect(self.exit)
        self.setIcon(QIcon(":images/img/tray_logo.png"))
        self.setContextMenu(menu)


        self.list_replace=QmyListPlace()
        dialog=QDialog()
        self.list_replace.ui.setupUi(dialog)

        self.re_list=self.list_replace.getTableContent()

        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.fun)

        self.setToolTip("修正从MarginNote脑图中复制出来的汉字编码")
        self.showMessage("Message", "Running!")


    def fun(self):
        if self.clipboard.mimeData().hasText():
            # print("a:",self.table.item(0,0))
            text = self.clipboard.text()
            tmp = normalize("NFKC", text)
            new_tex = "".join([pattern.pattern[x] if x in pattern.pattern else x for x in list(tmp)])
            if text != new_tex:
                cl.copy(new_tex)
                comparison = {a: b for a, b in zip(list(text), list(new_tex)) if a != b}
                self.showMessage("替换列表：", json.dumps(comparison, ensure_ascii=False))
            # print(text)
            # print(new_tex)


    def setting(self):
        status = self.list_replace.exec()
        if status == QDialog.Accepted:
            self.re_list=self.list_replace.getTableContent()


    def exit(self):
        qApp.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWidget=MyWidget()
    myWidget.show()
    sys.exit(app.exec_())