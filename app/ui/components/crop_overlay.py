from PyQt5.QtWidgets import QWidget, QRubberBand
from PyQt5.QtCore import QRect, QPoint, QSize, Qt
from PyQt5.QtGui import QPainter, QColor, QPen

class CropOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # マウスイベントを透過
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

    def start_cropping(self):
        self.origin = None
        self.rubber_band.hide()

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubber_band.setGeometry(QRect(self.origin, QSize()))
        self.rubber_band.show()  # rubber_band を表示
        self.update()
        print(f"Mouse pressed at {self.origin}")

    def mouseMoveEvent(self, event):
        self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
        self.update()  # ウィジェットを再描画
        print(f"Mouse moved to {event.pos()}")

    def mouseReleaseEvent(self, event):
        self.rubber_band.hide()
        rect = self.rubber_band.geometry()
        self.crop_rect = (rect.x(), rect.y(), rect.width(), rect.height())
        print(f"Selected area: {self.crop_rect}")

    def paintEvent(self, event):
        painter = QPainter(self)

        # 枠線の太さを設定
        pen = QPen(QColor(255, 0, 0), 5)  # 赤、太さ5
        painter.setPen(pen)

        # 塗りつぶしをなしに設定
        painter.setBrush(Qt.NoBrush)  

        print("paintEvent called")
        print(f"rubber_band geometry: {self.rubber_band.geometry()}")
        print(f"rubber_band isVisible: {self.rubber_band.isVisible()}")
        print(f"painter pen: {painter.pen()}")
        print(f"painter brush: {painter.brush()}")

        painter.drawRect(self.rubber_band.geometry())
