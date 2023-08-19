import sys
from PyQt5 import QtWidgets, QtCore, QtGui

import envs
from datalens.api import envs as api_envs
from datalens.api import api_utils

class ImageInfosUI(QtWidgets.QDialog):
    def __init__(self, path=None):
        super().__init__()
        if path:
            self._path = path
            self._exif = api_utils.get_exifs(path)
        else:
            self._path = ""

        self.setWindowTitle("Image Details")
        self.resize(1000, 600)

        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        # Image buttons
        self.add_image_btn = QtWidgets.QPushButton("Add Image(JPG,PNG)")
        self.add_image_btn.clicked.connect(self.on_add_image_clicked)
        self.add_brut_btn = QtWidgets.QPushButton("Add Brut(JPG,PNG)")

        # Image
        self.image_lbl = QtWidgets.QWidget()

        # in the grids
        self.subject_le = QtWidgets.QLineEdit()
        self.description_le = QtWidgets.QLineEdit()
        self.date_le = QtWidgets.QDateEdit()
        self.date_le.setDisplayFormat("yyyy, MM, dd")
        self.location_le = QtWidgets.QLineEdit()
        self.lights_le = QtWidgets.QSpinBox()
        self.lights_le.setMaximum(9999)
        self.exposure_le = QtWidgets.QDoubleSpinBox()
        self.exposure_le.setMaximum(9999.9999)
        self.focal_le = QtWidgets.QDoubleSpinBox()
        self.focal_le.setMaximum(9999.9)
        self.iso_le = QtWidgets.QSpinBox()
        self.iso_le.setMaximum(99999)
        self.aperture_le = QtWidgets.QDoubleSpinBox()
        self.aperture_le.setMaximum(99.9)
        self.maker_le = QtWidgets.QLineEdit()
        self.model_le = QtWidgets.QLineEdit()
        
        self.mount_le = QtWidgets.QLineEdit()
        self.process_le = QtWidgets.QLineEdit()
        self.author_le = QtWidgets.QLineEdit()
        self.comment_le = QtWidgets.QLineEdit()

        # Button
        self.ok_btn = QtWidgets.QPushButton("Add image")
        self.ok_btn.clicked.connect(self._accept)
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.deleteLater)
        
    def create_layouts(self):
        # Main layout
        main_layout = QtWidgets.QHBoxLayout(self)

        # Images
        adds_layout = QtWidgets.QHBoxLayout()
        if not self._path:
            adds_layout.addWidget(self.add_image_btn)
            adds_layout.addWidget(self.add_brut_btn)

        self.v_image_layout = QtWidgets.QVBoxLayout()
        self.v_image_layout.addLayout(adds_layout)

        main_layout.addLayout(self.v_image_layout)

        # Grids
        v_layout = QtWidgets.QVBoxLayout()
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
        aperture_lbl = QtWidgets.QLabel(envs.G_F_NUMBER)
        # equipment
        maker_lbl = QtWidgets.QLabel(envs.G_MAKE)
        model_lbl = QtWidgets.QLabel(envs.G_MODEL)
        focal_lbl = QtWidgets.QLabel(envs.G_FOCAL)
        mount_lbl = QtWidgets.QLabel(envs.A_MOUNT)
        # 
        author_lbl = QtWidgets.QLabel(envs.G_AUTHOR)
        process_lbl = QtWidgets.QLabel(envs.G_SOFTWARE)
        comment_lbl = QtWidgets.QLabel(envs.G_COMMENT)
        
        font_bold = QtGui.QFont("Arial", 8, QtGui.QFont.Bold)
        for column_lbl in [subject_lbl, desc_lbl, date_lbl, location_lbl, lights_lbl,
                           exposure_lbl, iso_lbl, aperture_lbl,
                           focal_lbl, mount_lbl, author_lbl, model_lbl,
                           maker_lbl, process_lbl, comment_lbl]:
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
        for label, wdg in zip([maker_lbl,model_lbl, focal_lbl, mount_lbl],
                              [self.maker_le, self.model_le, self.focal_le, self.mount_le]):
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
        if not self._path:
            h_layout.addWidget(self.ok_btn)
            h_layout.addWidget(self.cancel_btn)
        h_layout.addStretch(1)
        v_layout.addLayout(h_layout)
 
    def _update(self):
        self.v_image_layout.removeWidget(self.image_lbl)

        self.subject_le.setText(self._exif.get(api_envs.SUBJECT, ""))
        self.description_le.setText(self._exif.get(api_envs.DESC, ""))
        try:
            date = [int(d) for d in self._exif.get(api_envs.DATE).split(" ")[0].split(":")]
            q_date = QtCore.QDate(date[0], date[1], date[2])
        except:
            q_date = QtCore.QDate.currentDate()
        self.date_le.setDate(q_date)
        self.location_le.setText(self._exif.get(api_envs.LOCATION, ""))
        self.exposure_le.setValue(float(self._exif.get(api_envs.EXPOSURE_TIME, 0)))
        self.focal_le.setValue(float(self._exif.get(api_envs.FOCAL, 0)))
        self.iso_le.setValue(int(self._exif.get(api_envs.ISO, 0)))
        self.aperture_le.setValue(float(self._exif.get(api_envs.F_NUMBER, 0)))
        self.author_le.setText(self._exif.get(api_envs.AUTHOR, ""))
        self.maker_le.setText(self._exif.get(api_envs.MAKE,""))
        self.model_le.setText(self._exif.get(api_envs.MODEL,""))
        self.comment_le.setText(self._exif.get(api_envs.COMMENT,""))
        self.process_le.setText(self._exif.get(api_envs.SOFTWARE))

        self.image_lbl = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(self._exif.get(api_envs.PATH))
        pixmap = pixmap.scaled(700, 500, QtCore.Qt.KeepAspectRatio)
        self.image_lbl.setPixmap(pixmap)
        self.v_image_layout.addWidget(self.image_lbl)

    def _accept(self):
        self.deleteLater()
        self.accept()
        
    def open_file_dialog(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            return file_dialog.selectedFiles()[0] # temp

    def read(self):
        return {api_envs.ID : self._exif.get(api_envs.ID),
                api_envs.SUBJECT : self.subject_le.text(),
                api_envs.PATH : self._exif.get(api_envs.PATH),
                api_envs.DESC : self.description_le.text(),
                api_envs.MAKE : self.maker_le.text(),
                api_envs.MODEL : self.model_le.text(),
                api_envs.MOUNT : self.mount_le.text(),
                api_envs.FOCAL : self.focal_le.value(),
                api_envs.F_NUMBER : self.aperture_le.value(),
                api_envs.ISO : self.iso_le.value(),
                api_envs.LIGHTS : self.lights_le.value(),
                api_envs.EXPOSURE_TIME : self.exposure_le.value(),
                api_envs.LOCATION : self.location_le.text(),
                api_envs.BORTLE : 0,
                api_envs.MOON_PHASE : 0,
                api_envs.SOFTWARE : self.process_le.text(),
                api_envs.AUTHOR : self.author_le.text(),
                api_envs.COMMENT : self.comment_le.text(),
                api_envs.DATE : self.date_le.text()}
    
    def on_add_image_clicked(self):
        path = self.open_file_dialog()
        self._exif = api_utils.get_exifs(path)
        self._update()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ImageInfosUI()
    window.show()
    sys.exit(app.exec_())
