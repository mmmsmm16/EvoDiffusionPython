from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt
from app.ui.components.crop_button import CropButton
from app.ui.components.crop_overlay import CropOverlay

class ImageDisplay(QWidget):
    def __init__(self, parent=None, button_position="right", app=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        
        # 画像
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setFixedSize(512, 512)

        # CropOverlay の追加
        self.crop_overlay = CropOverlay(self.image_label)
        self.crop_overlay.setGeometry(self.image_label.rect())
        self.crop_overlay.show()  # 常に表示

        # 評価ボタンのレイアウト
        self.evaluation_layout = QVBoxLayout()
        self.evaluation_layout.setSpacing(10)
        self.evaluation_buttons = []

        button = QPushButton("select", self)
        self.is_selected = False
        button.setCheckable(True)
        button.clicked.connect(lambda checked, button=button: self.on_evaluation_button_clicked(checked, button))
        self.evaluation_buttons.append(button)
        self.evaluation_layout.addWidget(button)

        # Crop ボタンの追加
        self.crop_button = CropButton(self, self)
        self.evaluation_layout.addWidget(self.crop_button)

        # メインレイアウト
        main_layout = QHBoxLayout(self)
        if button_position == "left":
            main_layout.addLayout(self.evaluation_layout)
            main_layout.addWidget(self.image_label)
        else:
            main_layout.addWidget(self.image_label)
            main_layout.addLayout(self.evaluation_layout)

        print(f"ImageDisplay initialized. Geometry: {self.geometry()}")

    def set_pixmap(self, pixmap):
        self.image_label.setPixmap(pixmap)
        self.update()
        print("Pixmap set")

    def start_cropping(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.CrossCursor))
        self.crop_overlay.start_cropping()
        print("Cropping started in ImageDisplay")

    def stop_cropping(self):
        QApplication.restoreOverrideCursor()
        self.crop_overlay.stop_cropping()
        print("Cropping stopped in ImageDisplay")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.crop_overlay.setGeometry(self.image_label.rect())
        print(f"ImageDisplay resized. New geometry: {self.geometry()}")

    def showEvent(self, event):
        super().showEvent(event)
        print(f"ImageDisplay shown. Geometry: {self.geometry()}")

    def get_selected_rect(self):
        return self.crop_overlay.get_selected_rect()
