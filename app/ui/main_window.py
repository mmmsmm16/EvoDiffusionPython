import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QProgressBar, QTextEdit, QRadioButton, QButtonGroup, QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from app.ui.componets.image_display import ImageDisplay


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EvoDiffusionPython")
        self.setGeometry(100, 1000, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 画像表示領域
        image_layout = QGridLayout()
        self.image_displays = []
        for i in range(4):
            image_display = ImageDisplay()
            self.image_displays.append(image_display)
            image_layout.addWidget(image_display, i // 2, i % 2)

        # 操作ボタン
        button_layout = QHBoxLayout()
        button_names = ["Generate"]  # 修正ボタンを削除
        self.buttons = {}
        for name in button_names:
            button = QPushButton(name)
            self.buttons[name] = button
            button_layout.addWidget(button)
        layout.addLayout(button_layout)

        # 進捗バー
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # テキスト出力領域（デバッグ用）
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        # イベントハンドラの接続 (後で実装)
        # ...

    # 画像更新メソッド (後で実装)
    def update_images(self, image_paths):
        for i, path in enumerate(image_paths):
            pixmap = QPixmap(path)
            self.image_labels[i].setPixmap(pixmap)

    # その他のメソッド (後で実装)
    def on_evaluation_button_clicked(self, checked, button):  # メソッドを追加
        if checked:
            button.setText("Selected")
        else:
            button.setText("Select")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
