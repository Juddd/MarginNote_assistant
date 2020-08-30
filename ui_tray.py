from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog,QMenu
import sys
import imgs_rc
from mylistplace import Ui_ListReplace

class Tray():
    def setupUi(self,Ui_Tray):
        menu = QMenu()
        settingAction = menu.addAction("设置")
        settingAction.triggered.connect(self.setting)
        exitAction = menu.addAction("退出")
        exitAction.triggered.connect(sys.exit)

        icon=QIcon(":images/tray_logo.png")
        Ui_Tray.setIcon(icon)
        Ui_Tray.setContextMenu(menu)
        Ui_Tray.setToolTip("修正从MarginNote脑图中复制出来的汉字编码")
        Ui_Tray.showMessage("Message", "Running!")

    def setting(self):
        self.dialog = Ui_ListReplace()

        self.table=Ui_Dialog()
        self.table.setupUi(self.dialog)
        # self.dialog.re.connect(self.dialog.close())
        self.dialog.show()
    # def setting(self):
    #     dialog=MyDialog()
    #     dialog.show()



