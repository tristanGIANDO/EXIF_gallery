import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

from api.exif_file import ExifFile
import envs

class ImageInfosUI(QtWidgets.QDialog):
    def __init__(self, path):
        super().__init__()
        self._path = path
        self._exif = ExifFile(path)

        self.setWindowTitle("Image Data")
        self.resize(700, 900)

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

        # in the grids
        self.date_le = QtWidgets.QLineEdit()
        self.location_le = QtWidgets.QLineEdit()
        self.lights_le = QtWidgets.QLineEdit()
        self.exposure_le = QtWidgets.QLineEdit()
        self.focal_le = QtWidgets.QLineEdit()
        self.iso_le = QtWidgets.QLineEdit()
        self.aperture_le = QtWidgets.QLineEdit()
        self.camera_le = QtWidgets.QLineEdit()
        
        self.mount_le = QtWidgets.QLineEdit()
        self.process_le = QtWidgets.QLineEdit()
        self.author_le = QtWidgets.QLineEdit()

        # Button
        self.ok_btn = QtWidgets.QPushButton("Add image")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        
    def create_layouts(self):
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addWidget(self.image_lbl, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.title_le, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.description_le, alignment=Qt.AlignCenter)
        
        # Labels
        # acquisition
        date_lbl = QtWidgets.QLabel(envs.G_DATE)
        location_lbl = QtWidgets.QLabel(envs.G_LOCATION)
        lights_lbl = QtWidgets.QLabel(envs.A_LIGHTS)
        exposure_lbl = QtWidgets.QLabel(envs.G_EXPOSURE_TIME)
        iso_lbl = QtWidgets.QLabel(envs.G_ISO)
        aperture_lbl = QtWidgets.QLabel(envs.G_APERTURE)
        # equipment
        camera_lbl = QtWidgets.QLabel(envs.G_CAMERA)
        focal_lbl = QtWidgets.QLabel(envs.G_FOCAL)
        mount_lbl = QtWidgets.QLabel(envs.A_MOUNT)
        # 
        author_lbl = QtWidgets.QLabel(envs.G_AUTHOR)
        process_lbl = QtWidgets.QLabel(envs.G_PROCESS)
        
        font_bold = QFont("Arial", 8, QFont.Bold)
        for column_lbl in [date_lbl, location_lbl, lights_lbl,
                           exposure_lbl, iso_lbl, aperture_lbl,
                           focal_lbl, mount_lbl, author_lbl, camera_lbl,
                           process_lbl]:
                column_lbl.setFont(font_bold)

        # Acquisition grid
        acquisition_gb = QtWidgets.QGroupBox("Acquisition Details")
        grid_layout = QtWidgets.QGridLayout(acquisition_gb)
        
        pos = 0
        for label, wdg in zip([date_lbl, location_lbl, lights_lbl,
                               exposure_lbl, iso_lbl, aperture_lbl],
                              [self.date_le, self.location_le, self.lights_le,
                               self.exposure_le, self.iso_le, self.aperture_le]):
            grid_layout.addWidget(label, pos, 0)
            grid_layout.addWidget(wdg, pos, 1)
            pos += 1
 
        main_layout.addWidget(acquisition_gb)

        # Equipment grid
        equipment_gb = QtWidgets.QGroupBox("Equipment Details")
        grid_layout = QtWidgets.QGridLayout(equipment_gb)
        
        pos = 0
        for label, wdg in zip([camera_lbl, focal_lbl, mount_lbl],
                              [self.camera_le, self.focal_le, self.mount_le]):
            grid_layout.addWidget(label, pos, 0)
            grid_layout.addWidget(wdg, pos, 1)
            pos += 1
 
        main_layout.addWidget(equipment_gb)

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
