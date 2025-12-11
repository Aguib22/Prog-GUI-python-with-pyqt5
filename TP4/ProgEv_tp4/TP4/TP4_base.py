import sys
from PyQt5.QtWidgets import *
from MyComponents import MyWidget_exo2 as exo1
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
import os



class MyImageViewerWidget(QFrame):

    def __init__(self, *args):

        super(MyImageViewerWidget, self).__init__(*args)
        self.setGeometry(0, 0, 800, 600)
        self.ui = exo1.Ui_Form()
        self.ui.setupUi(self)
        self.timer = QTimer(self)
    def LoadFiles(self):
        print("Loading files...")
        path = str(QFileDialog.getExistingDirectoryUrl(self, "Select Directory").toLocalFile())
        if not path:
           return
        
        print("chemin de l'image:", path)
        self.ui.mLineEdit.setText(path)

        self.image_files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

        if len(self.image_files) == 0:
            QMessageBox.warning("Aucune image trouvé.")
            return

        self.current_index = 0
        self.print_image()

    def print_image(self):
        if not hasattr(self, 'image_files') or len(self.image_files) == 0:
            return
        
        image_path = os.path.join(self.ui.mLineEdit.text(), self.image_files[self.current_index])
        pixmap = QPixmap(image_path)
        self.ui.mlabel.setPixmap(pixmap.scaled(self.ui.mlabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
       


    def Next(self):
        print("Next image")
        if not hasattr(self, 'image_files') or len(self.image_files) == 0:
            return
        self.current_index = (self.current_index + 1) % len(self.image_files)
        self.print_image()

    def Previous(self):
        print("Previous image")
        if not hasattr(self, 'image_files') or len(self.image_files) == 0:
            return
        self.current_index = (self.current_index - 1) % len(self.image_files)
        self.print_image()

    def Animate(self):
        print("Animate")
        self.timer.timeout.connect(self.Next)
        if self.ui.startTimer.isChecked():
            self.ui.startTimer.setText("Stop")
            self.timer.start(1000)  # Change image every second
        else:
            self.ui.startTimer.setText("Start")
            self.timer.stop()

class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        # attributs de la fenetre principale
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle('Simple diaporama application')

        # donnée membre qui contiendra la frame associée à la widget crée par QtDesigner
        self.mDisplay = MyImageViewerWidget(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()