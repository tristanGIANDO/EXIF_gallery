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

        self.setWindowTitle("Image Details")
        self.resize(1000, 600)

        self.create_widgets()
        self.create_layouts()
        self.set_default_values()

    def create_widgets(self):
        # Image
        self.image_lbl = QtWidgets.QLabel()
        pixmap = QPixmap(self._path)
        pixmap = pixmap.scaled(700, 500, Qt.KeepAspectRatio)
        self.image_lbl.setPixmap(pixmap)

        # in the grids
        self.subject_le = QtWidgets.QLineEdit()
        self.description_le = QtWidgets.QLineEdit()
        self.date_le = QtWidgets.QDateEdit()
        self.location_le = QtWidgets.QLineEdit()
        self.lights_le = QtWidgets.QSpinBox()
        self.exposure_le = QtWidgets.QSpinBox()
        self.focal_le = QtWidgets.QSpinBox()
        self.iso_le = QtWidgets.QSpinBox()
        self.aperture_le = QtWidgets.QDoubleSpinBox()
        self.camera_le = QtWidgets.QLineEdit()
        
        self.mount_le = QtWidgets.QLineEdit()
        self.process_le = QtWidgets.QLineEdit()
        self.author_le = QtWidgets.QLineEdit()
        self.comment_le = QtWidgets.QLineEdit()

        # Button
        self.ok_btn = QtWidgets.QPushButton("Add image")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.close)
        
    def create_layouts(self):
        # Main layout
        main_layout = QtWidgets.QHBoxLayout(self)
        v_layout = QtWidgets.QVBoxLayout()

        main_layout.addWidget(self.image_lbl, alignment=Qt.AlignCenter)
        main_layout.addLayout(v_layout)
        
        # Labels
        subject_lbl = QtWidgets.QLabel(envs.G_SUBJECT)
        desc_lbl = QtWidgets.QLabel(envs.G_DESC)
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
        comment_lbl = QtWidgets.QLabel(envs.G_COMMENT)
        
        font_bold = QFont("Arial", 8, QFont.Bold)
        for column_lbl in [subject_lbl, desc_lbl, date_lbl, location_lbl, lights_lbl,
                           exposure_lbl, iso_lbl, aperture_lbl,
                           focal_lbl, mount_lbl, author_lbl, camera_lbl,
                           process_lbl, comment_lbl]:
                column_lbl.setFont(font_bold)

        # global grid
        global_gb = QtWidgets.QGroupBox()
        grid_layout = QtWidgets.QGridLayout(global_gb)
        
        pos = 0
        for label, wdg in zip([subject_lbl, desc_lbl],
                              [self.subject_le, self.description_le]):
            grid_layout.addWidget(label, pos, 0)
            grid_layout.addWidget(wdg, pos, 1)
            pos += 1
 
        v_layout.addWidget(global_gb)

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
 
        v_layout.addWidget(acquisition_gb)

        # Equipment grid
        equipment_gb = QtWidgets.QGroupBox("Equipment Details")
        grid_layout = QtWidgets.QGridLayout(equipment_gb)
        
        pos = 0
        for label, wdg in zip([camera_lbl, focal_lbl, mount_lbl],
                              [self.camera_le, self.focal_le, self.mount_le]):
            grid_layout.addWidget(label, pos, 0)
            grid_layout.addWidget(wdg, pos, 1)
            pos += 1
 
        v_layout.addWidget(equipment_gb)

        # more grid
        more_gb = QtWidgets.QGroupBox("More info")
        grid_layout = QtWidgets.QGridLayout(more_gb)
        
        pos = 0
        for label, wdg in zip([author_lbl, process_lbl, comment_lbl],
                              [self.author_le, self.process_le, self.comment_le]):
            grid_layout.addWidget(label, pos, 0)
            grid_layout.addWidget(wdg, pos, 1)
            pos += 1
 
        v_layout.addWidget(more_gb)

        # Buttons
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.ok_btn)
        h_layout.addWidget(self.cancel_btn)
        h_layout.addStretch(1)
        v_layout.addLayout(h_layout)
 
    def set_default_values(self):
        self.subject_le.setText(self._exif.get_name())
        self.description_le.setText(self._exif.get_description())
        self.author_le.setText(self._exif.get_author())
        self.camera_le.setText(self._exif.get_camera())
        self.comment_le.setText(self._exif.get_comment())

    def read(self):
        return {"id" : self._exif.get_id(),
                "subject" : self.subject_le.text(),
                "path" : self._path,
                "description" : self.description_le.text(),
                "camera" : self.camera_le.text(),
                "mount" : self.mount_le.text(),
                "focal" : int(input(self.focal_le.text())),
                "aperture" : float(input(self.aperture_le.text())),
                "iso" : int(input(self.iso_le.text())),
                "lights" : int(input(self.lights_le.text())),
                "exposure" : int(input(self.exposure_le.text())),
                "place" : self.location_le.text(),
                "bortle" : 0,
                "moon" : 0,
                "process" : self.process_le.text(),
                "author" : self.author_le.text(),
                "comment" : self.comment_le.text(),
                "date" : self.date_le.text()}

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ImageInfosUI(r"C:\Users\giand\OneDrive\Images\@PORTFOLIO\230219_m31_04.jpg")
    window.show()
    sys.exit(app.exec_())
