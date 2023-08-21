import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QColorDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen, QImage, QFont
from PyQt5.QtCore import Qt, QRectF

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Viewer')
        self.setGeometry(100, 100, 1200, 800)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setGeometry(20, 20, 1000, 1000)

        self.graphics_view = QGraphicsView(self)
        self.graphics_view.setGeometry(1040, 20, 140, 140)

        self.scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.scene)

        self.pen_color = Qt.red
        self.pen_size = 2

        self.pixmap = None
        self.pixmap_item = None

        self.painter = None

        self.draw_button = QPushButton('Draw', self)
        self.draw_button.setGeometry(1040, 180, 140, 40)
        self.draw_button.clicked.connect(self.start_drawing)

        self.save_button = QPushButton('Save', self)
        self.save_button.setGeometry(1040, 240, 140, 40)
        self.save_button.clicked.connect(self.save_image)

        self.clear_button = QPushButton('Clear', self)
        self.clear_button.setGeometry(1040, 300, 140, 40)
        self.clear_button.clicked.connect(self.clear_image)

        self.load_button = QPushButton('Load Image', self)
        self.load_button.setGeometry(1040, 360, 140, 40)
        self.load_button.clicked.connect(self.load_image)

    def start_drawing(self):
        if self.pixmap:
            self.painter = QPainter(self.pixmap)
            self.painter.setRenderHint(QPainter.Antialiasing)
            self.painter.setPen(QPen(self.pen_color, self.pen_size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.painter:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.painter:
            self.painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update_display()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.painter:
            self.painter.end()
            self.update_display()

    def update_display(self):
        self.pixmap_item.setPixmap(self.pixmap)
        self.image_label.setPixmap(self.pixmap)

    def save_image(self):
        if self.pixmap:
            image_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'PNG Images (*.png);;All Files (*)')
            if image_path:
                self.pixmap.save(image_path)

    def clear_image(self):
        if self.pixmap:
            self.pixmap.fill(Qt.white)
            self.update_display()

    def load_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)')
        if image_path:
            image = QPixmap(image_path)
            self.pixmap = image.copy()  # Make a copy to preserve the original image
            if self.pixmap_item:
                self.scene.removeItem(self.pixmap_item)
            self.pixmap_item = QGraphicsPixmapItem(self.pixmap)
            self.scene.addItem(self.pixmap_item)
            self.painter = QPainter(self.pixmap)
            self.update_display()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())