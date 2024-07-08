from PyQt5.QtWidgets import QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageDisplay(QWidget):
    def __init__(self, parent=None, button_position="right"):  # button_position 引数を追加
        super().__init__(parent)

        # 画像
        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setFixedSize(512, 512)

        # 評価ボタンのレイアウト
        self.evaluation_layout = QVBoxLayout()
        self.evaluation_layout.setSpacing(10)
        self.evaluation_buttons = []

        button = QPushButton("select", self)
        self.is_selected = False # 選択状態を保持するフラグ
        button.setCheckable(True)
        button.clicked.connect(lambda checked, button=button: self.on_evaluation_button_clicked(checked, button))
        self.evaluation_buttons.append(button)
        self.evaluation_layout.addWidget(button)

        # レイアウトの設定 (QHBoxLayout を使用)
        layout = QHBoxLayout()
        self.setLayout(layout)

        # button_position に応じて評価ボタンを配置
        if button_position == "left":
            layout.addLayout(self.evaluation_layout)
            layout.addWidget(self.image_label)
        else:  # default は right
            layout.addWidget(self.image_label)
            layout.addLayout(self.evaluation_layout)
    
    def set_pixmap(self, pixmap):
        self.image_label.setPixmap(pixmap)  
    
    def on_evaluation_button_clicked(self, checked, button):
        self.is_selected = checked
        if checked:
            button.setText("Selected")
        else:
            button.setText("Select")

        # 他の評価ボタンを解除
        for btn in self.evaluation_buttons:
            if btn != button:
                btn.setChecked(False)
                btn.setText("Select")
