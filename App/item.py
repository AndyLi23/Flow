from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Item(QWidget):
    def __init__(self, parent):
        super(Item, self).__init__()
                
        self.setParent(parent)        
        
        self.start = QPoint(50, 50)
        self.pressing = False

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
                        
        self.setGeometry(30, 30, 330, 110)
        
        self.p = QLabel("")
        
        self.title = QLineEdit(self.p)
        self.title.move(22, 20)
        self.title.setFrame(False);
        
        self.title.setProperty("cssClass", "title")
        self.title.setAttribute(Qt.WA_MacShowFocusRect, 0)
        
        self.title.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(self.p)
        
        self.setLayout(self.layout)
                
        self.setStyleSheet("""
            
            QLabel {
                background: url(../assets/b.png) no-repeat center center fixed;
                border-radius: 20px;
            }   

            *[cssClass="title"] {     
                background-color: rgba(0,0,0,0);       
                padding: 3px;
                color: #382606;
                border: none;
                font-size: 30px;
                font-family: times;
                min-height: 40px;
                max-height: 40px;
                margin: 0;
                max-width: 250px;
                min-width: 250px;
            }    
            *[cssClass="title"]:focus {
                background-color: rgba(0,0,0,0.1);    
            }

        """)
        
        self.show()

        
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
        
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.setGeometry(self.x() + self.movement.x(),
                                self.y() + self.movement.y(),
                                self.width(),
                                self.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False