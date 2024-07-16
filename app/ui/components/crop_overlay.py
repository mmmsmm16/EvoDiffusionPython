from PyQt5.QtWidgets import QWidget, QRubberBand
from PyQt5.QtCore import QRect, QPoint, QSize, Qt
from PyQt5.QtGui import QPainter, QColor, QPen

class CropOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setMouseTracking(True)
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.is_cropping = False
        self.selected_rect = None
        self.setStyleSheet("background-color: rgba(255, 255, 255, 50);")

    def start_cropping(self):
        self.is_cropping = True
        self.setCursor(Qt.CrossCursor)
        self.selected_rect = None  # 新しいクロッピングを開始するときに以前の選択をクリア
        self.update()
        print("Cropping started")

    def stop_cropping(self):
        self.is_cropping = False
        self.unsetCursor()
        self.rubber_band.hide()
        if self.rubber_band.geometry().isValid():
            self.selected_rect = self.rubber_band.geometry()
        self.update()
        print("Cropping stopped")

    def mousePressEvent(self, event):
        if self.is_cropping and event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()
            print(f"Mouse pressed at {self.origin}")

    def mouseMoveEvent(self, event):
        if self.is_cropping and not self.origin.isNull():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
            print(f"Mouse moved to {event.pos()}")

    def mouseReleaseEvent(self, event):
        if self.is_cropping and event.button() == Qt.LeftButton:
            self.rubber_band.hide()
            self.selected_rect = self.rubber_band.geometry()
            print(f"Selected area: {self.selected_rect}")
            self.stop_cropping()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0), 2, Qt.SolidLine)
        painter.setPen(pen)
        
        if self.rubber_band.isVisible():
            painter.drawRect(self.rubber_band.geometry())
        elif self.selected_rect:
            painter.drawRect(self.selected_rect)

    def showEvent(self, event):
        super().showEvent(event)
        print(f"CropOverlay shown. Geometry: {self.geometry()}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        print(f"CropOverlay resized. New geometry: {self.geometry()}")

    def get_selected_rect(self):
        return self.selected_rect
