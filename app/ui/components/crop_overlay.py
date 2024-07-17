from PyQt5.QtWidgets import QWidget, QRubberBand
from PyQt5.QtCore import QRect, QPoint, QSize, Qt
from PyQt5.QtGui import QPainter, QColor, QPen

class CropOverlay(QWidget):
    """
    画像上にクロッピング領域を表示し、ユーザーの選択を管理するオーバーレイウィジェット
    
    このクラスは、マウスイベントを処理して矩形選択を可能にし、選択された領域を視覚的に表示する
    """

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
        """クロッピング操作の開始"""
        self.is_cropping = True
        self.setCursor(Qt.CrossCursor)
        self.selected_rect = None
        self.update()

    def stop_cropping(self):
        """クロッピング操作の終了"""
        self.is_cropping = False
        self.unsetCursor()
        self.rubber_band.hide()
        if self.rubber_band.geometry().isValid():
            self.selected_rect = self.rubber_band.geometry()
        self.update()

    def mousePressEvent(self, event):
        """マウスボタンが押されたときの処理"""
        if self.is_cropping and event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()

    def mouseMoveEvent(self, event):
        """マウスが移動したときの処理"""
        if self.is_cropping and not self.origin.isNull():
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        """マウスボタンが離されたときの処理"""
        if self.is_cropping and event.button() == Qt.LeftButton:
            self.rubber_band.hide()
            self.selected_rect = self.rubber_band.geometry()
            self.stop_cropping()

    def paintEvent(self, event):
        """ウィジェットの描画処理"""
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(255, 0, 0), 2, Qt.SolidLine)
        painter.setPen(pen)
        
        if self.rubber_band.isVisible():
            painter.drawRect(self.rubber_band.geometry())
        elif self.selected_rect:
            painter.drawRect(self.selected_rect)

    def get_selected_rect(self):
        """選択された矩形を取得"""
        return self.selected_rect
