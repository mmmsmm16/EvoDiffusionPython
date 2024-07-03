import sys

from PyQt5.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from PyQt5.QtGui import QFontDatabase

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
