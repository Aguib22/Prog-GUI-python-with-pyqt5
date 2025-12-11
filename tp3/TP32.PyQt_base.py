import sys
import os
import random
import pickle
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QStatusBar, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QFile, QIODevice, Qt
from PyQt5.QtGui import QPainter, QBrush, QPen


class myHisto:
    """Classe myHisto pour stocker l'histogramme"""

    def __init__(self):
        print('Méthode __init__()  de la classe myHisto')
        self.m_list = []   # valeurs de chaque bin
        self.m_size = 0    # nombre de bins
        self.m_max = 0     # valeur max (pour l’échelle verticale)

    def load_from_file(self, path):
        """Charge l'histogramme depuis un fichier texte .dat (10 lignes, 1 valeur par ligne)"""
        f = QFile(path)
        if not f.open(QIODevice.ReadOnly | QIODevice.Text):
            print("Erreur : impossible d'ouvrir le fichier", path)
            return False

        # réinitialiser
        self.m_list = []
        self.m_size = 0
        self.m_max = 0

        # lire ligne par ligne
        while not f.atEnd():
            line = bytes(f.readLine()).decode('utf-8').strip()
            if not line:
                continue
            try:
                val = int(line)
            except ValueError:
                continue
            self.m_list.append(val)

        f.close()

        self.m_size = len(self.m_list)
        self.m_max = max(self.m_list) if self.m_list else 0

        print("Histogramme chargé :", self.m_list, "max =", self.m_max)
        return True

    def reset_zero(self, size=10):
        """Remet l'histogramme à zéro (size bins à 0)."""
        self.m_list = [0] * size
        self.m_size = size
        # on met max à 1 pour éviter division par 0 dans paintEvent
        self.m_max = 1

    def random_init(self, size=10):
        """Initialise l'histogramme avec des valeurs aléatoires entre 0 et 99."""
        self.m_list = [random.randint(0, 99) for _ in range(size)]
        self.m_size = size
        self.m_max = max(self.m_list) if self.m_list else 0
        print("Histogramme aléatoire :", self.m_list, "max =", self.m_max)


class MyMainWindow(QMainWindow):
    """ Classe de l'application principale"""

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)

        # Attributs de la fenetre principale
        self.setGeometry(300, 300, 600, 450)
        self.titleInfo = "VOTRE_NOM"
        self.titleMainWindow = self.titleInfo + datetime.now().strftime(
            "  %H:%M:%S") + ' | Res: ' + str(self.width()) + 'x' + str(self.height())
        self.setWindowTitle(self.titleMainWindow)

        # Barre de status
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Zone d'informations, peut toujours servir")

        # Histogramme
        self.mHisto = myHisto()

        # Drag & Drop activé
        self.setAcceptDrops(True)

        self.createActions()
        self.createMenus()

    # ---------- mise à jour du titre à chaque resize ----------
    def resizeEvent(self, event):
        self.titleMainWindow = self.titleInfo + datetime.now().strftime(
            "  %H:%M:%S") + ' | Res: ' + str(self.width()) + 'x' + str(self.height())
        self.setWindowTitle(self.titleMainWindow)
        super().resizeEvent(event)

    # ---------- actions ----------
    def createActions(self):
        # Menu File
        self.openAct = QAction("&Open...", self)
        self.openAct.setShortcut("Ctrl+O")
        self.openAct.triggered.connect(self.myOpen)

        self.saveAct = QAction("&Save...", self)
        self.saveAct.setShortcut("Ctrl+S")
        self.saveAct.triggered.connect(self.mySave)

        self.restoreAct = QAction("&Restore...", self)
        self.restoreAct.setShortcut("Ctrl+R")
        self.restoreAct.triggered.connect(self.myRestore)

        self.exitAct = QAction("&Bye...", self)
        self.exitAct.setShortcut("Ctrl+B")
        self.exitAct.triggered.connect(self.myExit)

        # Menu Display
        self.clearAct = QAction("&Clear", self)
        self.clearAct.setShortcut("Ctrl+L")
        self.clearAct.triggered.connect(self.myClear)

        self.colorAct = QAction("&Color", self)
        self.colorAct.setShortcut("Ctrl+C")
        self.colorAct.triggered.connect(self.myColor)

        self.lureAct = QAction("&Lure", self)  # item demandé
        self.lureAct.setShortcut("Ctrl+U")
        self.lureAct.triggered.connect(self.myOpen)  # comme Open

    # ---------- menus ----------
    def createMenus(self):
        menubar = self.menuBar()

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(self.openAct)
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.restoreAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        displayMenu = menubar.addMenu("&Display")
        displayMenu.addAction(self.lureAct)
        displayMenu.addAction(self.clearAct)
        displayMenu.addAction(self.colorAct)

    # ---------- slots File ----------
    def myOpen(self):
        """Ouvre un fichier .dat et charge l'histogramme"""
        base_dir = os.path.dirname(os.path.abspath(__file__))

        fname, _ = QFileDialog.getOpenFileName(
            self,
            "Open histogram file",
            base_dir,
            "Data files (*.dat);;All files (*)"
        )

        if not fname:
            return

        if self.mHisto.load_from_file(fname):
            self.statusBar.showMessage("Histogram opened !")
            self.update()
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de charger le fichier sélectionné.")

    def mySave(self):
        """Sérialise m_list dans saveHisto.bin (pickle.dump)."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(base_dir, "saveHisto.bin")

        try:
            with open(save_path, "wb") as f:
                pickle.dump(self.mHisto.m_list, f)
            self.statusBar.showMessage("Histogram saved !")
        except Exception as e:
            print("Erreur save:", e)
            QMessageBox.warning(self, "Erreur", "Impossible de sauvegarder l'histogramme.")

    def myRestore(self):
        """Restaure m_list depuis saveHisto.bin (pickle.load)."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(base_dir, "saveHisto.bin")

        if not os.path.exists(save_path):
            QMessageBox.warning(self, "Erreur", "Aucune sauvegarde trouvée (saveHisto.bin).")
            return

        try:
            with open(save_path, "rb") as f:
                data = pickle.load(f)
            if not isinstance(data, list):
                raise ValueError("format invalide")
            self.mHisto.m_list = data
            self.mHisto.m_size = len(data)
            self.mHisto.m_max = max(data) if data else 0
            self.statusBar.showMessage("Histogram restored !")
            self.update()
        except Exception as e:
            print("Erreur restore:", e)
            QMessageBox.warning(self, "Erreur", "Impossible de restaurer l'histogramme.")

    def myExit(self):
        self.statusBar.showMessage("Quit ...")
        QApplication.quit()

    # ---------- slots Display ----------
    def myClear(self):
        """Remise à zéro de l'histogramme via Clear : affiche 'Lure !'."""
        self.mHisto.reset_zero()
        self.statusBar.showMessage("Lure !")
        self.update()

    def myColor(self):
        # Pour l’instant, on ne change pas la couleur, on montre juste qu'on réagit.
        self.statusBar.showMessage("Color changed !")

    # ---------- Drag & Drop ----------
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return

        path = urls[0].toLocalFile()
        self.statusBar.showMessage(f"Drop file: {path}")

        if self.mHisto.load_from_file(path):
            self.statusBar.showMessage("Histogram opened ! (drag & drop)")
            self.update()
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de charger le fichier déposé.")

    # ---------- gestion de la touche R ----------
    def keyPressEvent(self, event):
        """Touche 'R' : initialisation aléatoire de l'histogramme."""
        if event.key() == Qt.Key_R:
            self.mHisto.random_init()
            self.statusBar.showMessage("Histogram randomized (R key) !")
            self.update()
        else:
            # comportement standard pour les autres touches
            super().keyPressEvent(event)

    # ---------- dessin de l'histogramme ----------
    def paintEvent(self, event):
        """Dessine l'histogramme en rouge, adapté à la taille de la fenêtre"""

        if self.mHisto.m_size == 0 or self.mHisto.m_max == 0:
            return  # rien à dessiner

        painter = QPainter(self)

        # Style : contour noir, remplissage rouge
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.red))

        # Géométrie (on garde des marges)
        full_w = self.width()
        full_h = self.height()

        top_margin = 30
        bottom_margin = 40
        left_margin = 10
        right_margin = 10

        w = full_w - left_margin - right_margin
        h = full_h - top_margin - bottom_margin
        if w <= 0 or h <= 0:
            return

        n = self.mHisto.m_size
        bin_width = int(w / n)
        max_val = self.mHisto.m_max

        for i, val in enumerate(self.mHisto.m_list):
            rect_height = int((val / max_val) * h)   # échelle verticale
            x = left_margin + i * bin_width          # position en X
            y = top_margin + (h - rect_height)       # position en Y

            painter.drawRect(x, y, bin_width - 2, rect_height)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()
