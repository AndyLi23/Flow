from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import playsound



class App(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
                
        self.setGeometry(0, 0, 1080, 720)
        self.setStylesheet()
        self.initUI()

    def initUI(self):        
        
        self.page = QWidget()

        self.tab = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignBottom)
        self.add = QLabel("+")
        layout.addWidget(self.add)
        layout.setContentsMargins(0, 0, 0, 0)
        
        
        self.tab.setLayout(layout)
        
        self.tab.setStyleSheet("""
            QWidget {
                margin: 0px;
            }
            QLabel {
                font-size: 100px;
                padding: 10px;
                color: #444;
                background-color: #fff;
            }
        """)

        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.page.setLayout(layout)
        
        
        self.setCentralWidget(self.page)
        
        self.page.setStyleSheet("""

        """)
        
        
        self.show()

    def setStylesheet(self):
        self.setStyleSheet("""
        QWidget {
            background: #fff;
        }
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
