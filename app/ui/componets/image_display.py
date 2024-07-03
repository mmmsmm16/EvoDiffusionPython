from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageDisplay(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)  # 画像のアスペクト比を維持して拡大・縮小
        self.setStyleSheet("border: 1px solid black;")
        self.setFixedSize(512, 512)

        # 評価ボタンのレイアウト
        self.evaluation_layout = QVBoxLayout()
        self.evaluation_layout.setSpacing(10)  # ボタン間の間隔を設定 (任意の値に変更可能)
        self.evaluation_buttons = []
        for evaluation in ["1", "2", "3", "4", "5"]:
            button = QPushButton(evaluation, self)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, button=button: self.on_evaluation_button_clicked(checked, button))
            self.evaluation_buttons.append(button)
            self.evaluation_layout.addWidget(button)

        # レイアウトの設定
        layout = QHBoxLayout()  # 画像と評価ボタンを横に並べる
        self.setAlignment(Qt.AlignCenter)  # 画像を中央に配置

        # 左側の画像には評価ボタンを左に、右側の画像には評価ボタンを右に配置
        if self.parent() is not None and self.parent().indexOf(self) % 2 == 0:  # 左側の画像
            layout.addLayout(self.evaluation_layout)
            layout.addWidget(self)
        else:  # 右側の画像
            layout.addWidget(self)
            layout.addLayout(self.evaluation_layout)

        self.setLayout(layout)

    def set_pixmap(self, pixmap):
        self.setPixmap(pixmap)

    def on_evaluation_button_clicked(self, checked, button):
        if checked:
            button.setText("Selected")
        else:
            button.setText("Select")

        # 他の評価ボタンを解除
        for btn in self.evaluation_buttons:
            if btn != button:
                btn.setChecked(False)
                btn.setText("Select")

