from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

class CropButton(QPushButton):
    def __init__(self, parent=None, image_display=None):  # image_display 引数を追加
        super().__init__("Crop", parent)
        self.image_display = image_display  # ImageDisplay インスタンスを保持
        self.setCheckable(True)
        self.clicked.connect(self.on_clicked)

    def on_clicked(self, checked):
        if checked:
            self.setText("Cropping")
            self.image_display.start_cropping()  # ImageDisplay の start_cropping メソッドを呼び出す
        else:
            self.setText("Crop")
            self.image_display.stop_cropping()
