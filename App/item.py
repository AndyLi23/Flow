from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Item(QWidget):
    def __init__(self, parent, window):
        super(Item, self).__init__()
                
        self.setParent(parent)     
        
        if(len(window.curPos) == 0):
            window.curPos.append(0)
        else:
            window.curPos.append(window.curPos[-1]+1)
            
        self.order = window.curPos[-1]
        
        self.children = []
                
        self.setGeometry(30+20*self.order, 30+20*self.order, 320, 120)
            
        self.window = window
        
        self.start = QPoint(50, 50)
        self.pressing = False

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignTop)
                                
        self.p = QLabel("")
        self.p.setProperty("cssClass", "main")
        
        self.title = QLineEdit(self.p)
        self.title.move(32, 30)
        self.title.setFrame(False);
        
        self.title.setProperty("cssClass", "title")
        self.title.setAttribute(Qt.WA_MacShowFocusRect, 0)
        
        self.close = QPushButton("x")
        self.close.move(10, 0)
        self.close.pressed.connect(self.delete)
        
        self.add = QPushButton("+")
        self.add.move(25, 90)
        self.add.pressed.connect(self.addChild)
        
        self.title.setAlignment(Qt.AlignCenter)
        
        
        self.s = QLabel("", self)
        self.s.setProperty("cssClass", "stick")
        self.s.move(30, 20)
                
        self.layout.addWidget(self.p)
        
        self.setLayout(self.layout)
                
        self.set_Stylesheet(100)
        
        self.show()
        self.close.setParent(self)
        self.add.setParent(self)
        
        self.close.show()
        self.add.show()

        
    
    def addChild(self):
        n = len(self.children) + 1
        print(n)
        self.setGeometry(self.x(), self.y(), 320, 130 + 80*n)
        self.set_Stylesheet(110 + 80*n)
        self.add.move(25, 95+80*n)
        
        new = QLabel("", self)
        new.setGeometry(10, 30+80*n, 250, 70)
        new.show()
        self.children.append(new)

    def set_Stylesheet(self, n):
        s = """
            QLabel {
                border-image: url(../assets/b.png) 0 0 0 0 stretch stretch;
                border-radius: 20px;
                background-color: rgba(0,0,0,0);
            }  
            
            *[cssClass="main"] {
                max-height: 100px;
                min-height: 100px;
            }
            
            *[cssClass="stick"] {
                border-image: url(../assets/c.png) 0 0 0 0 stretch stretch;
                max-width: 20px;
                min-width: 20px;
                min-height: %spx;
            }

            *[cssClass="title"] {     
                background-color: rgba(0,0,0,0);       
                padding: 3px;
                color: #382606;
                border: none;
                font-size: 35px;
                min-height: 40px;
                max-height: 40px;
                margin: 0;
                font-weight: 500;
                max-width: 250px;
                min-width: 250px;
            }    
            *[cssClass="title"]:focus {
                background-color: rgba(0,0,0,0.1);    
            }
            
            QPushButton {
                background: none;
                border: none;
                min-height: 30px;
                max-height: 30px;
                min-width: 30px;
                max-width: 30px;
                font-size: 30px;
                color: #593a00;
            }

        """ % (str(n))
        
        self.setStyleSheet(s)
            
        
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True
        
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        self.end = self.mapToGlobal(event.pos()) - self.window.pos()
        if self.end.x() < 0 or self.end.y() < 28 or self.end.x() > self.window.width() or self.end.y() > self.window.height() + 28:
            self.pressing = False            
        
        
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            
            if self.x() + self.movement.x() < 0:
                self.movement.setX(0)
            if self.y() + self.movement.y() < 0:
                self.movement.setY(0)
            if self.x() + self.movement.x() > self.window.width() - self.width():
                self.movement.setX(0)
            if self.y() + self.movement.y() > self.window.height() - self.height():
                self.movement.setY(0)
            
            self.setGeometry(self.x() + self.movement.x(),
                                self.y() + self.movement.y(),
                                self.width(),
                                self.height())
            self.start = self.end
            
            if(self.movement.x() > 0 or self.movement.y() > 0):
                if self.order in self.window.curPos:
                    self.window.curPos.remove(self.order)
                    

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False
        
    def delete(self):
        if self.order in self.window.curPos:
            self.window.curPos.remove(self.order)
        self.close.deleteLater()
        self.deleteLater()