import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QProgressBar, QTextEdit, QRadioButton, QButtonGroup, QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from app.ui.components.image_display import ImageDisplay


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
            # 左側の画像には評価ボタンを左に、右側の画像には評価ボタンを右に配置
            button_position = "left" if i % 2 == 0 else "right"
            image_display = ImageDisplay(button_position=button_position)
            self.image_displays.append(image_display)  # ImageDisplay インスタンスをリストに追加
            image_layout.addWidget(image_display, i // 2, i % 2)  # image_layout に追加
        layout.addLayout(image_layout)

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

        # 初期画像を設定
        images_path = ['app/data/test/0.png', 'app/data/test/1.png', 'app/data/test/2.png', 'app/data/test/3.png']
        for i, image_display in enumerate(self.image_displays):
            pixmap = QPixmap(images_path[i])
            if pixmap.isNull():  # 画像の読み込みに失敗した場合
                print(f"Failed to load image: {images_path[i]}")
            else:
                image_display.set_pixmap(pixmap)

     # 画像更新メソッド
    def update_images(self, image_paths):
        for i, path in enumerate(image_paths):
            pixmap = QPixmap(path)
            self.image_displays[i].set_pixmap(pixmap)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
