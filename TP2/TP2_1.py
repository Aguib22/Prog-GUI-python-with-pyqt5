# ...existing code...
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
        self.setMinimumSize(400, 200)  # taille minimale
        self.initUI()   # appel d'une methode dédiée à la création de l'IHM

        # état pour le tracé et coordonnées du dernier clic
        self.doPaint = False
        self.autoPaint = False
        self.x = 0
        self.y = 0
        self.paintCount = 0

        self.init_w = 800
        self.init_h = 400

    def initUI(self):
        # création des boutons sans layout (parent = self)
        self.btnDessine = QPushButton("Dessine", self)
        self.btnDessine.setGeometry(10, 10, 90, 30)
        self.btnDessine.clicked.connect(self.on_draw)

        self.btnEfface = QPushButton("Efface", self)
        self.btnEfface.setGeometry(10, 50, 90, 30)
        self.btnEfface.clicked.connect(self.on_clear)

        # optionnel : raccourcis visibles
        self.btnDessine.setToolTip("D - dessine la grille")
        self.btnEfface.setToolTip("E - efface la grille")

    def on_draw(self):
        self.doPaint = True
        self.update()  # forcer rafraîchissement

    def on_clear(self):
        self.doPaint = False
        self.update()

    def paintEvent(self, event):
        # compteur d'événements Paint
        self.paintCount += 1
        print("paintEvent count: " + str(self.paintCount))

        qp = QPainter()
        qp.begin(self)

        # Mettre à jour le titre avec la taille actuelle
        w = self.width()
        h = self.height()
        self.setWindowTitle(f"SOW - {w} x {h}")

        # Si doPaint est actif, tracer la grille et les lettres
        if self.doPaint:
            # ligne horizontale au milieu
            mid_y = h // 2
            qp.drawLine(0, mid_y, w, mid_y)

            # 12 lignes verticales (13 colonnes)
            cols = 13
            for i in range(1, cols):
                x = int(i * w / cols)
                qp.drawLine(x, 0, x, h)

            
            cell_w = w / cols
            cell_h = h / 2
            code = ord('A')
            # font = qp.font()
            # #augmenter la taille si souhaité
            # font.setPointSize(max(10, int(min(cell_w, cell_h) // 4)))
            # qp.setFont(font)

            for row in range(2):
                for col in range(cols):
                    if code > ord('Z'):
                        break
                    x0 = int(col * cell_w)
                    y0 = int(row * cell_h)
                    cell_rect = QRect(x0, y0, int(cell_w), int(cell_h))
                    qp.drawText(cell_rect, Qt.AlignCenter, chr(code))
                    code += 1

        # Si doPaint est False, on n'effectue aucun dessin (les boutons restent visibles car widgets enfants)
        qp.end()

    def mouseReleaseEvent(self, event):
        # mémoriser position du clic (utile pour la suite du TP)
        self.x = event.x()
        self.y = event.y()
        print("click: x=" + str(self.x) + " y=" + str(self.y))

        # si la grille est affichée, déterminer la case et afficher la lettre correspondante
        if self.doPaint:
            w = self.width()
            h = self.height()
            cols = 13
            cell_w = w / cols
            cell_h = h / 2

            # calculer colonne et ligne (clamp pour rester dans les bornes)
            col = int(self.x // cell_w)
            col = max(0, min(cols-1, col))
            row = 0 if self.y < cell_h else 1

            index = row * cols + col
            if 0 <= index <= (ord('Z') - ord('A')):
                letter = chr(ord('A') + index)
                print(f"Letter clicked: {letter}")
        # provoquer un rafraîchissement pour afficher tout changement éventuel
        self.update()

    def keyPressEvent(self, event):
        # touches D pour dessiner, E pour effacer
        if event.key() == Qt.Key_D:
            self.on_draw()
        elif event.key() == Qt.Key_E:
            self.on_clear()
        else:
            # laisser la gestion par défaut pour les autres touches
            super().keyPressEvent(event)

    def resizeEvent(self, event):
        # détecte le redimensionnement et active automatiquement la grille
        w = self.width()
        h = self.height()
       
        if w <= self.init_w // 2 or h <= self.init_h // 2:
            if not self.doPaint:
                self.doPaint = True
                self.autoPaint = True
                self.update()
        else:
            if self.autoPaint:
                self.doPaint = False
                self.autoPaint = False
                self.update()
        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = myMainWindow() 
    w.show() 
    sys.exit(app.exec_())
# ...existing code...