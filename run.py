import sys
from unicodedata import normalize
import clipboard as cl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication,QMenu,QSystemTrayIcon,QTableWidget,QLabel,QLineEdit,QHeaderView
import res
import json

pattern = {
	"⼞": "口",
    "⺒": "巳",
    "⺎": "兀",
    "⺏": "尣",
    "⺓": "幺",
    "⺔": "彑",
    "⺛": "旡",
    "⺝": "月",
    "⺞": "歺",
    "⺟": "母",
    "⺠": "民",
    "⺢": "氺",
    "⺩": "王",
    "⺬": "示",
    "⺯": "糹",
    "⺽": "臼",
    "⺾": "艹",
    "⻁": "虎",
    "⻃": "覀",
    "⻄": "西",
    "⻆": "角",
    "⻈": "讠",
    "⻋": "车",
    "⻑": "長",
    "⻒": "镸",
    "⻖": "阝",
    "⻘": "青",
    "⻙": "韦",
    "⻚": "页",
    "⻛": "风",
    "⻜": "飞",
    "⻝": "食",
    "⻢": "马",
    "⻣": "骨",
    "⻤": "鬼",
    "⻥": "鱼",
    "⻦": "鸟",
    "⻧": "卤",
    "⻩": "黄",
    "⻪": "黾",
    "⻫": "斉",
    "⻬": "齐",
    "⻭": "歯",
    "⻮": "齿",
    "⻯": "竜",
    "⻰": "龙",
    "⻱": "龜",
    "⻲": "亀",
    "⻳": "龟"
}


class Tray:
    def __init__(self):
        self.app = QApplication(sys.argv)
        icon = QIcon(":res/image.png")

        menu = QMenu()

        exitAction = menu.addAction("退出")
        exitAction.triggered.connect(sys.exit)

        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.fun)

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip("修正从MarginNote脑图中复制出来的汉字编码")
        self.tray.showMessage("Message", "Running!")

    def run(self):
        self.app.exec_()
        sys.exit()

    def fun(self):
        if self.clipboard.mimeData().hasText():
            text = self.clipboard.text()
            tmp=normalize("NFKC", text)
            new_tex = "".join([pattern[x] if x in pattern else x for x in list(tmp)])
            if text != new_tex:
                cl.copy(new_tex)
                comparison={a:b for a,b in zip(list(text),list(new_tex)) if a != b}
                self.tray.showMessage("替换列表：",json.dumps(comparison,ensure_ascii=False))
            # print(text)
            # print(new_tex)

if __name__ == "__main__":
    app = Tray()
    app.run()
