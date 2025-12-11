import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("this's my first pyqt5 app")

window.setMinimumSize(350,250)
window.setMaximumSize(800,600)
window.show()
window.setGeometry(800,800,500,400)

sys.exit(app.exec_())