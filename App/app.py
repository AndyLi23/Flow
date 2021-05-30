from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from item import Item
import json


class App(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        
        self.items = []


        self.mainLayout = QVBoxLayout()      
        self.setMaximumSize(2000, 1200)
        
        self.curPos = []
                
        self.setGeometry(0, 0, 1080, 720)
        self.setStylesheet()
        self.initUI()

    def initUI(self):
        self.initPage()

        self.page = QWidget()

        self.mainLayout.setAlignment(Qt.AlignLeft)
        self.mainLayout.addWidget(self.tab)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        

        self.page.setLayout(self.mainLayout)
        
        self.setCentralWidget(self.page)

        with open("../assets/data/a.json", "r") as fin:
            data = json.loads(fin.read())
            for item in data["items"]:
                self.addItem(item)
                
            self.curPos = data["order"]

        self.show()

    def setStylesheet(self):
        self.setStyleSheet("""
        QMainWindow {
            background: url(../assets/a.jpg) no-repeat center center fixed;
            
        }
        """)

    def initPage(self):
        self.tab = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignBottom)
        self.add = QPushButton("+")
        
        self.add.clicked.connect(lambda: self.addItem(None))

        layout.addWidget(self.add)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tab.setLayout(layout)

        self.tab.setStyleSheet("""
            QWidget {
                margin: 0px;
            }
            QPushButton {
                font-size: 100px;
                color: #e0c575;
                height: 100px;
                width: 100px;
                background: none;
                border: none;
            }
            
            QPushButton:pressed {
                color: #a68b3d;
            }
        """)
        
    def addItem(self, data):
        w = Item(self.page, self, data)
        self.items.append(w)

        
    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)
        
    def closeEvent(self, event):
        with open("../assets/data/a.json", "w+") as fout:
            fout.write(json.dumps({"items": [i.getJsonData() for i in self.items], "order": self.curPos}))        
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
        
    sys.exit(app.exec_())
