# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, QRect, Qt
from MyComponents.MyWidget_exo2 import Ui_Form  # ton widget corrigé

class MyImageViewerWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Liste des images et index
        self.images = []
        self.image_index = 0
        self.patch_index = 0

        # Préparer les rectangles pour découper les imagettes 300x300
        self.rects = [QRect(x, y, 300, 300) for y in range(0,300, 300) for x in range(0, 300, 300)]

        # Connexions boutons
        self.ui.mButtonBrowse.clicked.connect(self.LoadFiles)
        self.ui.mButtonN.clicked.connect(self.Next)
        self.ui.mButtonP.clicked.connect(self.Previous)
        self.ui.mButtonAnimate.clicked.connect(self.Animate)

        # Timer pour animation
        self.timer = QTimer()
        self.timer.setInterval(int(1000/15))  # 15 fps
        self.timer.timeout.connect(self.next_patch)
        self.animation_count = 0

    # ----------------------------
    # Gestion fichiers
    # ----------------------------
    def LoadFiles(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folder:
            self.ui.mLineEdit.setText(folder)
            self.images = []
            for f in sorted(os.listdir(folder)):
                if f.lower().endswith('.jpg'):
                    pix = QPixmap(os.path.join(folder, f))
                    if not pix.isNull():
                        self.images.append(pix)
            self.image_index = 0
            self.patch_index = 0
            if self.images:
                self.show_image()

    def show_image(self):
        if not self.images:
            return
        pix = self.images[self.image_index]
        cropped = pix.copy(self.rects[self.patch_index])
        self.ui.mLabel.setPixmap(cropped.scaled(self.ui.mLabel.size(), Qt.KeepAspectRatio))

    def Next(self):
        if not self.images:
            return
        self.patch_index += 1
        if self.patch_index >= len(self.rects):
            self.patch_index = 0
            self.image_index = (self.image_index + 1) % len(self.images)
        self.show_image()

    def Previous(self):
        if not self.images:
            return
        self.patch_index -= 1
        if self.patch_index < 0:
            self.image_index = (self.image_index - 1 + len(self.images)) % len(self.images)
            self.patch_index = len(self.rects) - 1
        self.show_image()

    def Animate(self):
        if self.ui.mButtonAnimate.isChecked():
            self.ui.mButtonAnimate.setText("STOP")
            self.animation_count = 0
            self.timer.start()
        else:
            self.ui.mButtonAnimate.setText("START")
            self.timer.stop()

    def next_patch(self):
        self.Next()
        self.animation_count += 1
        if self.animation_count >= 60:  # 4 secondes à 15 fps
            self.timer.stop()
            self.ui.mButtonAnimate.setChecked(False)
            self.ui.mButtonAnimate.setText("START")
            self.animation_count = 0

    # ----------------------------
    # Touche S pour déclencher l’animation
    # ----------------------------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_S:
            if not self.timer.isActive():
                self.animation_count = 0
                self.timer.start()
                self.ui.mButtonAnimate.setChecked(True)
                self.ui.mButtonAnimate.setText("STOP")
        else:
            super().keyPressEvent(event)


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle('Diaporama application')
        self.mDisplay = MyImageViewerWidget(self)
        self.setCentralWidget(self.mDisplay)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
