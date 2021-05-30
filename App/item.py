from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Item(QWidget):
    def __init__(self, parent, window, data):
        super(Item, self).__init__()
                
        self.setParent(parent)     
        
        if(len(window.curPos) == 0):
            window.curPos.append(0)
        else:
            window.curPos.append(window.curPos[-1]+1)
            
        self.order = window.curPos[-1]
        
        self.children = []
            
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
        self.add.move(25, 95)
        self.add.pressed.connect(lambda: self.addChild(""))
        
        self.title.setAlignment(Qt.AlignCenter)
        
        
        self.s = QLabel("", self)
        self.s.setProperty("cssClass", "stick")
        self.s.move(30, 20)
                
        self.layout.addWidget(self.p)
        
        self.setLayout(self.layout)
                
        self.set_Stylesheet(110)
        
        
        if data:
            pos = data["pos"]
            self.setGeometry(pos[0], pos[1], 320, 130)
            
            self.title.setText(data["txt"])
            
            for child in data["children"]:
                self.addChild(child)
            
            
        else:
            self.setGeometry(30+20*self.order, 30+20*self.order, 320, 130)
        
        
        self.show()
        self.close.setParent(self)
        self.add.setParent(self)
        
        self.close.show()
        self.add.show()

        
    
    def addChild(self, text):
        n = len(self.children) + 1
        self.setGeometry(self.x(), self.y(), 320, 130 + 80*n)
        self.set_Stylesheet(110 + 80*n)
        self.add.move(25, 95+80*n)
        
        new = QLabel("", self)
        new.setGeometry(10, 30+80*n, 250, 70)
        
        close = QPushButton("x")
        close.move(5, 0)
        close.pressed.connect(lambda: self.deleteSub((new, close)))
        
        txt = QLineEdit(new)
        txt.move(22, 15)
        txt.setFrame(False);
        
        txt.setText(text)
        
        txt.setProperty("cssClass", "txt")
        txt.setAttribute(Qt.WA_MacShowFocusRect, 0)
        
        txt.setAlignment(Qt.AlignCenter)
        
        close.setParent(new)
        close.show()
        
        new.show()
        self.children.append((new, close, txt))

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
                max-height: %spx;
            }

            *[cssClass="title"] {     
                font-size: 35px;
                min-height: 40px;
                max-height: 40px;
                margin: 0;
                font-weight: 300;
                max-width: 250px;
                min-width: 250px;
            }    
            *[cssClass="txt"] {     
                font-size: 25px;
                min-height: 35px;
                max-height: 35px;
                margin: 0;
                font-weight: 100;
                max-width: 200px;
                min-width: 200px;
            } 
            QLineEdit {
                background-color: rgba(0,0,0,0);       
                padding: 3px;
                color: #382606;
                border: none;
            }
            QLineEdit:focus {
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

        """ % (str(n), str(n))
        
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
            
            if self.x() + self.movement.x() < -30 and not self.x() < -30:
                self.movement.setX(0)
            elif self.x() < -30 and self.movement.x() < 0:
                self.movement.setX(0)
            if self.y() + self.movement.y() < -30  and not self.y() < -30:
                self.movement.setY(0)
            elif self.y() < -30 and self.movement.y() < 0:
                self.movement.setY(0)
            if self.x() + self.movement.x() > self.window.width() - self.width() + 30 and not self.x() > self.window.width() - self.width() + 30:
                self.movement.setX(0)
            elif self.x() > self.window.width() - self.width() + 30 and self.movement.x() > 0:
                self.movement.setX(0)
            if self.y() + self.movement.y() > self.window.height() - self.height() + 30 and not self.y() > self.window.height() - self.height() + 30:
                self.movement.setY(0)
            elif self.y() > self.window.height() - self.height() + 30 and self.movement.y() > 0:
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
        
    def deleteSub(self, x):
        n = self.children.index(x)
        print(n)
        cur = self.children[n]
        cur[0].deleteLater()
        cur[1].deleteLater()
        
        for item in self.children[n+1:]:
            item[0].move(item[0].x(), item[0].y()-80)
            
        del self.children[n]
        
        self.set_Stylesheet(110 + 80*len(self.children))
            
        self.add.move(self.add.x(), self.add.y()-80)
        
        self.setGeometry(self.x(), self.y(), 320, 130 + 80*len(self.children))
        
    def getJsonData(self):
        ans = {}
        
        ans["pos"] = (self.x(), self.y())
        ans["txt"] = self.title.text()
        
        ans["children"] = [child[2].text() for child in self.children]
        
        return ans
        