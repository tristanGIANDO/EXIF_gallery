import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from api.exif_file import ExifFile

class ImageInfosUI(QtWidgets.QDialog):
    def __init__(self, path):
        super().__init__()
        self._path = path
        self._exif = ExifFile(path)

        self.setWindowTitle("Image Data")

        self.create_widgets()
        self.create_layouts()
        self.set_default_values()

    def create_widgets(self):
        # Image
        self.image_lbl = QtWidgets.QLabel()
        pixmap = QPixmap(self._path)
        pixmap = pixmap.scaled(690, 500, Qt.KeepAspectRatio)
        self.image_lbl.setPixmap(pixmap)

        # Title
        self.title_le = QtWidgets.QLineEdit()
        title_font = QFont("Arial", 18, QFont.Bold)  # Set font size to 18 and make it bold
        self.title_le.setFont(title_font)
        self.title_le.setAlignment(Qt.AlignCenter)

        # Description
        self.description_le = QtWidgets.QTextEdit("Description")

        # Button
        self.ok_btn = QtWidgets.QPushButton("Add image")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        
    def create_layouts(self):
        # Main layout
        main_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(self.image_lbl, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.title_le, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.description_le, alignment=Qt.AlignCenter)
        
        # EQUIPMENT GroupBox
        equipment_gb = QtWidgets.QGroupBox("Acquisition Details")
        grid_layout = QtWidgets.QGridLayout(equipment_gb)
        
        author_lbl = QtWidgets.QLabel("Author")
        camera_lbl = QtWidgets.QLabel("Camera")
        lens_lbl = QtWidgets.QLabel("Lens")
        font_bold = QFont("Arial", 8, QFont.Bold)
        for column_lbl in [author_lbl, camera_lbl, lens_lbl]:
                column_lbl.setFont(font_bold)

        self.author_le = QtWidgets.QLineEdit()
        self.camera_le = QtWidgets.QLineEdit()

        grid_layout.addWidget(author_lbl, 0, 0)
        grid_layout.addWidget(camera_lbl, 1, 0)
        grid_layout.addWidget(lens_lbl, 2, 0)
        grid_layout.addWidget(self.author_le, 0, 1)
        grid_layout.addWidget(self.camera_le, 1, 1)
        main_layout.addWidget(equipment_gb)

        # ASTRO GroupBox
        astro_gb = QtWidgets.QGroupBox("Sky & Moon")
        astro_grid_layout = QtWidgets.QGridLayout(astro_gb)
        
        moon_lbl = QtWidgets.QLabel("Moon Illumination")
        font_bold = QFont("Arial", 8, QFont.Bold)
        for column_lbl in [moon_lbl]:
                column_lbl.setFont(font_bold)

        self.moon_le = QtWidgets.QLineEdit()

        astro_grid_layout.addWidget(moon_lbl, 0, 0)
        astro_grid_layout.addWidget(self.moon_le, 0, 1)
        main_layout.addWidget(astro_gb)

        # Comment Textfield
        main_layout.addWidget(QtWidgets.QLabel("Comment"))
        self.comment_le = QtWidgets.QLineEdit()
        main_layout.addWidget(self.comment_le)

        # Buttons
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.ok_btn)
        h_layout.addWidget(self.cancel_btn)
        h_layout.addStretch(1)
        main_layout.addLayout(h_layout)
        

        self.setLayout(main_layout)

    def set_default_values(self):
        self.title_le.setText(self._exif.get_name())
        self.description_le.setText(self._exif.get_description())
        self.author_le.setText(self._exif.get_author())
        self.camera_le.setText(self._exif.get_camera())
        self.comment_le.setText(self._exif.get_comment())

    def read(self):
        return {"id" : self._exif.get_id(),
                "subject" : self.title_le.text(),
                "path" : self._path,
                "description" : self.description_le.text(),
                "camera" : self.camera_le.text(),
                "mount" : "",
                "focal" : 0,
                "aperture" : 2.8,
                "iso" : self._exif.get_iso(),
                "lights" : 50,
                "exposure" : 120,
                "time" : 0,
                "place" : "",
                "bortle" : 0,
                "moon" : 0,
                "process" : "",
                "author" : self.author_le.text(),
                "comment" : self.comment_le.text(),
                "date" : self._exif.get_date()}

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ImageInfosUI(r"C:\Users\giand\OneDrive\Images\@PORTFOLIO\230219_m31_04.jpg")
    window.show()
    sys.exit(app.exec_())
