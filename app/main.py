import sys
from PyQt5.QtWidgets import QApplication
from app.ui.main_window import MainWindow

def main():
    """
    アプリケーションのメインエントリーポイント
    MainWindowを作成し、アプリケーションを実行する
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
