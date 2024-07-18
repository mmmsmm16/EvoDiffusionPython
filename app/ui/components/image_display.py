from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt
from app.ui.components.crop_button import CropButton
from app.ui.components.crop_overlay import CropOverlay

class ImageDisplay(QWidget):
    """
    画像表示とクロッピング機能を提供するウィジェット
    
    このクラスは、画像の表示、クロッピング操作、および評価ボタンの機能を統合
    また、画像の選択状態を追跡
    """

    def __init__(self, parent=None, button_position="right"):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        
        self.is_selected = False  # 選択状態を追跡する属性
        
        self._setup_image_label()
        self._setup_crop_overlay()
        self._setup_evaluation_button()
        self._setup_crop_button()
        self._setup_layout(button_position)

    def _setup_image_label(self):
        """画像表示用のラベルを設定"""
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setFixedSize(512, 512)

    def _setup_crop_overlay(self):
        """クロッピングオーバーレイを設定"""
        self.crop_overlay = CropOverlay(self.image_label)
        self.crop_overlay.setGeometry(self.image_label.rect())
        self.crop_overlay.show()

    def _setup_evaluation_button(self):
        """評価ボタンを設定"""
        self.evaluation_layout = QVBoxLayout()
        self.evaluation_layout.setSpacing(10)
        self.evaluation_buttons = []

        self.select_button = QPushButton("Select", self)
        self.select_button.setCheckable(True)
        self.select_button.clicked.connect(self._on_evaluation_button_clicked)
        self.evaluation_buttons.append(self.select_button)
        self.evaluation_layout.addWidget(self.select_button)

    def _setup_crop_button(self):
        """クロップボタンを設定"""
        self.crop_button = CropButton(self, self)
        self.evaluation_layout.addWidget(self.crop_button)

    def _setup_layout(self, button_position):
        """メインレイアウトを設定"""
        main_layout = QHBoxLayout(self)
        if button_position == "left":
            main_layout.addLayout(self.evaluation_layout)
            main_layout.addWidget(self.image_label)
        else:
            main_layout.addWidget(self.image_label)
            main_layout.addLayout(self.evaluation_layout)

    def set_pixmap(self, pixmap):
        """画像を設定"""
        self.image_label.setPixmap(pixmap)
        self.update()

    def start_cropping(self):
        """クロッピング操作を開始"""
        QApplication.setOverrideCursor(QCursor(Qt.CursorShape.CrossCursor))
        self.crop_overlay.start_cropping()

    def stop_cropping(self):
        """クロッピング操作を終了"""
        QApplication.restoreOverrideCursor()
        self.crop_overlay.stop_cropping()

    def _on_evaluation_button_clicked(self, checked):
        """評価ボタンがクリックされたときの処理"""
        self.is_selected = checked
        self.select_button.setText("Selected" if checked else "Select")

    def get_selected_rect(self):
        """選択された矩形を取得"""
        return self.crop_overlay.get_selected_rect()
    
    def reset_selection(self):
        """選択状態をリセットする"""
        self.is_selected = False
        self.select_button.setChecked(False)
        self.select_button.setText("Select")

    def reset_cropping(self):
        """クロッピング状態をリセットする"""
        self.crop_button.setChecked(False)
        self.crop_button.setText("Crop")
        self.crop_overlay.reset()

    def resizeEvent(self, event):
        """リサイズイベントの処理"""
        super().resizeEvent(event)
        self.crop_overlay.setGeometry(self.image_label.rect())

    def showEvent(self, event):
        """表示イベントの処理"""
        super().showEvent(event)
