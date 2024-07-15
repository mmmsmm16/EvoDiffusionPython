from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt
from app.ui.components.crop_button import CropButton
from app.ui.components.crop_overlay import CropOverlay

class ImageDisplay(QWidget):
    def __init__(self, parent=None, button_position="right", app=None):  # button_position 引数を追加
        super().__init__(parent)

        self.setStyleSheet("background-color: white;")  # 背景色を白に設定
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


         # Crop ボタンの追加
        self.crop_button = CropButton(self, self)
        self.evaluation_layout.addWidget(self.crop_button)

        # CropOverlay の追加 (一番上に配置)
        self.crop_overlay = CropOverlay(self)
        self.crop_overlay.setGeometry(self.geometry())
        layout.addWidget(self.crop_overlay)
        self.crop_overlay.show()  # CropOverlay を表示

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
        self.update()  # ImageDisplay を再描画
    
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

    def start_cropping(self):
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.CrossCursor))
        self.crop_overlay.setEnabled(True)  # CropOverlay を有効にする
        self.crop_overlay.start_cropping()


    def stop_cropping(self):
        QApplication.restoreOverrideCursor()
        # ここで self.crop_overlay.crop_rect を取得して保存する処理を追加
    
    def mousePressEvent(self, event):  # 追加
            if self.crop_button.isChecked():
                self.crop_overlay.mousePressEvent(event)

    def mouseMoveEvent(self, event):  # 追加
        if self.crop_button.isChecked():
            self.crop_overlay.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):  # 追加
        if self.crop_button.isChecked():
            self.crop_overlay.mouseReleaseEvent(event)
