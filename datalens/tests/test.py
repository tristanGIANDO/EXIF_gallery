import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QSlider, QScrollArea
from PyQt5.QtGui import QPixmap, QImage, QColor, QPainter
from PyQt5.QtCore import Qt
from pathlib import Path
from PIL import Image

class ImageViewer(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = str(self.resize_image(image_path, 500,300))
        self.scale_factor = 1.0
        self.brightness = 100
        self.saturation = 100

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Image Viewer")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.scroll_area.setWidget(self.image_label)
        
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.scroll_area)

        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(0)
        self.brightness_slider.setMaximum(200)
        self.brightness_slider.setValue(self.brightness)
        self.brightness_slider.valueChanged.connect(self.update_brightness)
        self.central_layout.addWidget(self.brightness_slider)

        self.saturation_slider = QSlider(Qt.Horizontal)
        self.saturation_slider.setMinimum(0)
        self.saturation_slider.setMaximum(200)
        self.saturation_slider.setValue(self.saturation)
        self.saturation_slider.valueChanged.connect(self.update_saturation)
        self.central_layout.addWidget(self.saturation_slider)

        self.load_image()
        self.show()

    def load_image(self):
        image = QImage(self.image_path)
        self.image_pixmap = QPixmap.fromImage(image)
        self.update_image()

    def update_image(self):
        image_copy = self.apply_brightness_and_saturation()
        self.image_label.setPixmap(image_copy)

    def apply_brightness_and_saturation(self):
        image = self.image_pixmap.toImage()
        width = image.width()
        height = image.height()

        for y in range(height):
            for x in range(width):
                pixel = QColor(image.pixel(x, y))
                brightness = min(255, max(0, pixel.lightness() + self.brightness - 100))
                saturation = min(255, max(0, pixel.saturation() + self.saturation - 100))
                pixel.setHsl(pixel.hslHue(), saturation, brightness)
                image.setPixel(x, y, pixel.rgb())

        return QPixmap.fromImage(image)

    def update_brightness(self, value):
        self.brightness = value
        self.update_image()

    def update_saturation(self, value):
        self.saturation = value
        self.update_image()

    def wheelEvent(self, event):
        num_degrees = event.angleDelta().y() / 8
        num_steps = num_degrees / 15.0
        self.scale_image(1.0 + num_steps * 0.1)

    def scale_image(self, factor):
        self.scale_factor *= factor
        if self.scale_factor < 1.0:
            self.scale_factor = 1.0
        if self.scale_factor > 2.0:
            self.scale_factor = 2.0
        new_width = self.image_pixmap.width() * self.scale_factor
        new_height = self.image_pixmap.height() * self.scale_factor
        self.image_label.setPixmap(self.image_pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio))

    def resize_image(self, path:str, w:int, h:int):
        path = Path(path)
        image = Image.open(path)
        image.thumbnail((w,h))
        result = path.parent / (path.stem + "_small" + path.suffix)
        image.save(result)
        
        return result

if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_path = r"C:\Users\giand\OneDrive\Images\@PORTFOLIO\230312_IMG_6716_F.jpg"
    viewer = ImageViewer(image_path)
    sys.exit(app.exec_())
