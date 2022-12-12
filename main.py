from PySide6.QtWidgets import QApplication
from mainwidget import MainWidget
import sys


app = QApplication(sys.argv)

window = MainWidget()

window.show()

app.exec()