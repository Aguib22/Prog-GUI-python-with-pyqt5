import sys
from PyQt5.QtWidgets import QApplication,QWidget


#creation d'une classe windows
class MyWindow(QWidget):
   
    def __init__(self,wind):
       super().__init__()
       self.wind = wind
       self.build()

    def build(self):
        self.setWindowTitle("my title")
        self.setGeometry(400,400,800,650)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    windInstace = MyWindow()
    windInstace.show()

    sys.exit(app.exec_())
