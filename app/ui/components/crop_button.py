from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

class CropButton(QPushButton):
    """
    クロッピング操作を開始/停止するためのボタン
    
    このボタンは、クリックされるとImageDisplayのクロッピング機能をトグルする役割を果たす
    """

    def __init__(self, parent=None, image_display=None):
        super().__init__("Crop", parent)
        self.image_display = image_display
        self.setCheckable(True)
        self.clicked.connect(self.on_clicked)

    def on_clicked(self, checked):
        """
        ボタンがクリックされたときの処理
        
        クロッピングモードを開始または停止し、ボタンのテキストを更新
        
        Args:
            checked (bool): ボタンがチェックされた状態かどうか
        """
        if checked:
            self.setText("Cropping")
            self.image_display.crop_overlay.start_cropping()
        else:
            self.setText("Crop")
            self.image_display.crop_overlay.stop_cropping()
            if not self.image_display.crop_overlay.selected_rect:
                self.image_display.crop_overlay.reset()
