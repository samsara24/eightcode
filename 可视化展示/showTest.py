import sys
from EightCodeShow import Ui_Dialog
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow

app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = Ui_Dialog()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec())