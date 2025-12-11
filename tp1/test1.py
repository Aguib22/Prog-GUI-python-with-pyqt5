from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.load(QUrl("test.qml"))

if not engine.rootObjects():
    print("Erreur de chargement QML")
    sys.exit(-1)

sys.exit(app.exec_())
