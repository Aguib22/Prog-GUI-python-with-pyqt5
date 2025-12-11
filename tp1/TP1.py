import sys
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIntValidator, QPainter, QPen, QPixmap, QColor

def GenerateSyracuseSequence(val):
    n = int(val)
    sequence = [n]
    if n > 1:
        max_val = n
        count = 1
        while n > 1:
            if n % 2 == 0:
                n = n // 2
            else:
                n = 3 * n + 1
            count += 1
            if n > max_val:
                max_val = n
            sequence.append(n)
        return sequence, count, max_val
    return sequence, 1, n

class MyMainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 300)
        title = "SOW" + datetime.now().strftime(" à  %H:%M:%S")
        self.setWindowTitle(title)

        self.entry_label = QLabel("Saisir un nombre et cliquer:")
        self.input_field = QLineEdit()
        self.input_field.setValidator(QIntValidator(1, 1000000, self))  
        self.result_label = QLabel("")
        self.bu = QPushButton("Calculer")

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        
        self.lb = QLabel()
        
        self.lb.setFixedHeight(300)
        self.lb.setFrameShape(QFrame.Panel)

        self.bu.clicked.connect(self.on_button_click)


        layout = QVBoxLayout(self)
        layout.addWidget(self.entry_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.bu)
        layout.addWidget(self.result_text)
        layout.addWidget(self.lb)
        
        self.setLayout(layout)

    def graphical_lin(self,values):
        w,h =self.lb.width(), self.lb.height()
        self.px = QPixmap(w,h)
        self.px.fill(QColor(200,200,200))
        paint = QPainter(self.px)
        pen = QPen(QColor(255,0,0))
        paint.setPen(pen) 
        if len(values)>1:
            for i in range(len(values)-1):
                x1 = i * (w / len(values))
                y1 = h - (values[i] / max(values)) * h
                x2 = (i+1) * (w / len(values))
                y2 = h - (values[i+1] / max(values)) * h
                paint.drawLine(int(x1), int(y1), int(x2), int(y2))
        paint.end()
        self.lb.setPixmap(self.px)


    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Quitter",
            "Etes vous sur de vouloir quitter?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def on_button_click(self):
        val = self.input_field.text()
        if val.isdigit() and int(val) > 0:
            values, count, max_val = GenerateSyracuseSequence(val)
            result_lines = [str(v) for v in values]
            result_lines.append(f"Nombre d'éléments: {count}")
            result_lines.append(f"Valeur la plus grande: {max_val}")
            self.result_text.setText('\n'.join(result_lines))

            self.graphical_lin(values)
        else:
           self.result_text.setText("Erreur : saisie invalide.\nVeuillez saisir un entier strictement positif.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.show()
    app.exec_()