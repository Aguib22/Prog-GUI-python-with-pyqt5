import sys
import urllib.request
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class myMainWindow(QWidget): 
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # attributs de la fenetre principale
        self.setGeometry(300,300,800,400)
        self.titlestart = "SOW " + datetime.now().strftime("  %H:%M:%S")
        self.setWindowTitle(self.titlestart) 
        self.rectUtil = self.rect()

        self.initUI()   # appel d'une methode dédiée à la création de l'IHM

        self.x = 0
        self.y = 0
        self.paintCount = 0
    def initUI(self):
        # L'affichage sur la console peut-être supprimé, il faudra completer ici pour la création d'autre elements IHM
        w = self.width()
        h = self.height()
        

    def paintEvent(self, event):
        self.paintCount += 1
        print("paintEvent count: " + str(self.paintCount))
        qp = QPainter()
        qp.begin(self)
        ract = self.rect()
        coord_click = '(x=0,y=0)' if (self.x == 0 and self.y == 0) else 'clic at: (x=' + str(self.x) + ', y=' + str(self.y)+')'
        qp.drawText(ract, Qt.AlignCenter, "Paint Event N°: " + str(self.paintCount)+" " + coord_click)
        qp.end()
    
    def mousePressEvent(self, event):
        self.x = event.x()
        self.y = event.y()
        print("click: x=" + str(self.x) + " y=" + str(self.y))
        self.update()   


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myMainWindow() 
    w.show() 
    app.exec_()    # ou de préférence sys.exit(app.exec_()) si vous êtes sous linux
