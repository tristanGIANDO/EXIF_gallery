import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui

from smoke.ui import envs
from smoke.api import envs as api_envs
from smoke.api import utils
from smoke.ui.features import WorldMapUI


# create inheritance and derive from / don't write "if", "elif"...
class ImageInfosUI(QtWidgets.QDialog):
    def __init__(self, author=None, album_type=None):
        super().__init__()
    
        self._exif = {}
        self._image_path = ""
        self._brut_path = ""
        if author:
            self._author = author
        else:
            self._author = ""

        self.setWindowTitle("Image Details")
        self.resize(1000, 600)
        self.setWindowIcon(envs.ICONS.get("logo"))

        # Image buttons
        self.add_image_btn = QtWidgets.QPushButton("Load Image(JPG,PNG)")
        self.add_image_btn.setIcon(envs.ICONS.get("add_file"))
        self.add_image_btn.setIconSize(QtCore.QSize(45,45))
        self.add_image_btn.clicked.connect(self.on_add_image_clicked)

        self.add_brut_btn = QtWidgets.QPushButton("Load Brut(JPG,PNG)")
        self.add_brut_btn.setIcon(envs.ICONS.get("add_file"))
        self.add_brut_btn.setIconSize(QtCore.QSize(45,45))
        self.add_brut_btn.clicked.connect(self.on_add_brut_clicked)

        self.location_btn = QtWidgets.QPushButton("Set Location")
        self.location_btn.clicked.connect(self.on_location_clicked)

        # Image
        self.image_lbl = QtWidgets.QLabel()
        self.brut_lbl = QtWidgets.QLabel()

        # Button
        self.ok_btn = QtWidgets.QPushButton("OK")
        self.ok_btn.setFixedSize(QtCore.QSize(80,30))
        self.ok_btn.clicked.connect(self._accept)
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.setFixedSize(QtCore.QSize(80,30))
        self.cancel_btn.clicked.connect(self.deleteLater)

        # Main layout
        self.main_layout = QtWidgets.QHBoxLayout(self)

        # Images
        adds_layout = QtWidgets.QHBoxLayout()
        adds_layout.addWidget(self.add_image_btn)
        # adds_layout.addWidget(self.add_brut_btn)

        self.v_image_layout = QtWidgets.QVBoxLayout()
        self.v_image_layout.addLayout(adds_layout)
        self.v_image_layout.addWidget(self.image_lbl)
        self.v_image_layout.addWidget(self.brut_lbl)

        self.main_layout.addLayout(self.v_image_layout)
        self.v_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.v_layout)

        # Labels
        self.subject_lbl = QtWidgets.QLabel(envs.G_SUBJECT)
        self.desc_lbl = QtWidgets.QLabel(envs.G_DESC)
        # acquisition
        self.date_lbl = QtWidgets.QLabel(envs.G_DATE)
        self.location_lbl = QtWidgets.QLabel(envs.G_LOCATION)
        self.exposure_lbl = QtWidgets.QLabel(envs.G_EXPOSURE_TIME)
        self.iso_lbl = QtWidgets.QLabel(envs.G_ISO)
        self.aperture_lbl = QtWidgets.QLabel(envs.G_F_NUMBER)
        # equipment
        self.maker_lbl = QtWidgets.QLabel(envs.G_MAKE)
        self.model_lbl = QtWidgets.QLabel(envs.G_MODEL)
        self.focal_lbl = QtWidgets.QLabel(envs.G_FOCAL)
        # 
        self.author_lbl = QtWidgets.QLabel(envs.G_AUTHOR)
        self.process_lbl = QtWidgets.QLabel(envs.G_SOFTWARE)
        self.comment_lbl = QtWidgets.QLabel(envs.G_COMMENT)

        # line edits
        self.subject_le = QtWidgets.QLineEdit()
        self.album_le = QtWidgets.QLineEdit()
        self.date_le = QtWidgets.QDateEdit()
        self.date_le.setDisplayFormat("yyyy, MM, dd")
        self.location_le = QtWidgets.QLineEdit()
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
        self.process_le = QtWidgets.QLineEdit()
        self.author_le = QtWidgets.QLineEdit()
        self.comment_le = QtWidgets.QLineEdit()

        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_layout.addWidget(self.ok_btn)
        self.h_layout.addWidget(self.cancel_btn)
        self.h_layout.addStretch(1)

        self.create_widgets()
        self.create_layouts()

        self.v_layout.addLayout(self.h_layout)

        self._update()

    def create_widgets(self):
        pass

    def create_layouts(self):
        pass
 
    def _update(self):
        # buttons
        if self._image_path:
            self.add_image_btn.setEnabled(False)
        else:
            self.add_image_btn.setEnabled(True)
        if self._brut_path:
            self.add_brut_btn.setEnabled(False)
        else:
            self.add_brut_btn.setEnabled(True)

        self.subject_le.setText(self._exif.get(api_envs.SUBJECT, "Subject"))
        self.album_le.setText(self._exif.get(api_envs.ALBUM, ""))
        try:
            date = [int(d) for d in self._exif.get(api_envs.DATE).split(" ")[0].split(":")]
            q_date = QtCore.QDate(date[0], date[1], date[2])
        except:
            q_date = QtCore.QDate.currentDate()
        self.date_le.setDate(q_date)
        self.location_le.setText(self._exif.get(api_envs.LOCATION, ""))
        
        self.exposure_le.setValue(float(self._exif.get(api_envs.EXPOSURE_TIME, 0.01)))
        self.focal_le.setValue(float(self._exif.get(api_envs.FOCAL, 35)))
        self.iso_le.setValue(int(self._exif.get(api_envs.ISO, 100)))
        self.aperture_le.setValue(float(self._exif.get(api_envs.F_NUMBER, 3.5)))
        self.author_le.setText(self._exif.get(api_envs.AUTHOR, self._author))
        self.maker_le.setText(self._exif.get(api_envs.MAKE,""))
        self.model_le.setText(self._exif.get(api_envs.MODEL,""))
        self.comment_le.setText(self._exif.get(api_envs.COMMENT,""))
        self.process_le.setText(self._exif.get(api_envs.SOFTWARE))

        # self.image_lbl = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(self._image_path)
        pixmap = pixmap.scaled(500, 300, QtCore.Qt.KeepAspectRatio)
        self.image_lbl.setPixmap(pixmap)
        # self.v_image_layout.addWidget(self.image_lbl)

        # self.brut_lbl = QtWidgets.QLabel()
        brut_pixmap = QtGui.QPixmap(self._brut_path)
        brut_pixmap = brut_pixmap.scaled(500, 300, QtCore.Qt.KeepAspectRatio)
        self.brut_lbl.setPixmap(brut_pixmap)
        # self.v_image_layout.addWidget(self.brut_lbl)

        self._type_update()

    def _type_update(self):
        pass

    def _accept(self):
        self.deleteLater()
        self.accept()
        
    def open_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp);;All Files (*)", options=options)

        if file_name:
            return file_name
        else:
            return ""

    def read(self):
        return {api_envs.ID : self._exif.get(api_envs.ID),
                api_envs.SUBJECT : self.subject_le.text(),
                api_envs.PATH : self._image_path,
                api_envs.ALBUM : self.album_le.text(),
                api_envs.MAKE : self.maker_le.text(),
                api_envs.MODEL : self.model_le.text(),
                api_envs.FOCAL : self.focal_le.value(),
                api_envs.F_NUMBER : self.aperture_le.value(),
                api_envs.ISO : self.iso_le.value(),
                api_envs.EXPOSURE_TIME : self.exposure_le.value(),
                api_envs.LOCATION : self.location_le.text(),
                api_envs.BORTLE : 0,
                api_envs.MOON_PHASE : 0,
                api_envs.SOFTWARE : self.process_le.text(),
                api_envs.AUTHOR : self.author_le.text(),
                api_envs.COMMENT : self.comment_le.text(),
                api_envs.DATE : self.date_le.text(),
                api_envs.PATH_BRUT : self._brut_path}
    
    def on_add_image_clicked(self):
        path = self.open_file_dialog()
        if path:
            self._image_path = path
            if not self._exif:
                self._exif = utils.get_exifs(path)
            self._update()
    
    def on_add_brut_clicked(self):
        path = self.open_file_dialog()
        if path:
            self._brut_path = path
            self._exif = utils.get_exifs(path)
            self._update()

    def on_location_clicked(self):
        ui = WorldMapUI()
        if ui.exec_():
            self.location_le.setText(ui.read())

class ImageViewerUI(QtWidgets.QDialog):
    def __init__(self, paths):
        super().__init__()
        if not paths:
            return
        
        self.setWindowTitle("Image Viewer")
        # self.resize(1600, 900)
        # self.setSizeGripEnabled(True)
        self.adjustSize()
        self.setWindowIcon(envs.ICONS.get("logo"))
        self.central_widget = QtWidgets.QWidget(self)

        self.layout = QtWidgets.QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.prev_button = QtWidgets.QPushButton(envs.ICONS.get("previous"), "")
        self.prev_button.setFixedSize(40,40)
        self.prev_button.setIconSize(QtCore.QSize(35,35))
        self.prev_button.clicked.connect(self.show_previous_image)
        self.layout.addWidget(self.prev_button)

        self.image_label = QtWidgets.QLabel(self)
        self.layout.addWidget(self.image_label)

        self.next_button = QtWidgets.QPushButton(envs.ICONS.get("next"), "")
        self.next_button.setFixedSize(40,40)
        self.next_button.setIconSize(QtCore.QSize(35,35))
        self.next_button.clicked.connect(self.show_next_image)
        self.layout.addWidget(self.next_button)

        self.image_paths = paths
        self.current_index = 0

        self.show_image()

    def show_image(self):
        if 0 <= self.current_index < len(self.image_paths):
            pixmap = QtGui.QPixmap(self.image_paths[self.current_index])
            pixmap = pixmap.scaled(1840, 1000, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(QtCore.Qt.AlignCenter)

            self.prev_button.setEnabled(self.current_index > 0)
            self.next_button.setEnabled(self.current_index < len(self.image_paths) - 1)

    def show_previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image()

    def show_next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.current_index += 1
            self.show_image()

class ThumbnailButton(QtWidgets.QPushButton):
    def __init__(self, db, path, size=None):
        super().__init__()
        if not size:
            size = (300,200)
        self.setFixedSize(size[0],size[1])

        self._db = db
        self.path = path
        self.parent_id = os.path.basename(os.path.dirname(self.path))
        self.parent_path = path.replace(api_envs.IMAGE_SMALL_SUFFIX, "")

        # get versions
        self._versions = [self.parent_path]
        self._versions += self._db._versions.get_versions_paths(self.parent_id)

        self.last_version = self._versions[-1]
        
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.load_image(self.last_version)

        version_button = QtWidgets.QPushButton(envs.ICONS.get("add_version"), "")
        version_button.setMaximumSize(40,40)
        version_button.setIconSize(QtCore.QSize(35,35))

        stacked_layout = QtWidgets.QStackedLayout()
        stacked_layout.setStackingMode(QtWidgets.QStackedLayout.StackingMode.StackAll)
        stacked_layout.addWidget(self.image_label)
        stacked_layout.addWidget(version_button)
        
        self.setLayout(stacked_layout)

        self.clicked.connect(self.on_image_clicked)
        version_button.clicked.connect(self.on_add_version_clicked)

    def open_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp);;All Files (*)",
            options=options
        )

        if file_name:
            return file_name
        else:
            return ""
    
    def load_image(self, image_path):
        splits = os.path.splitext(image_path)
        small_image_path = splits[0] + "-small" + splits[-1]
        print(small_image_path)
        if os.path.isfile(small_image_path):
            image_path = small_image_path
        pixmap = QtGui.QPixmap(image_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaledToHeight(
                self.height(),
                mode=QtCore.Qt.SmoothTransformation))
        else:
            self.image_label.setText("Failed to load image")
        
    def on_image_clicked(self):
        ui = ImageViewerUI(self._versions)
        ui.showFullScreen()
        ui.exec_()

    def on_add_version_clicked(self):
        path = self.open_file_dialog()
        if path:
            parent_dir = os.path.dirname(self.parent_path)
            filtered_files = [f for f in os.listdir(parent_dir) if "-" not in f]
            last_version_file = max(filtered_files)

            self._db._versions.insert_into(path, self.parent_id)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ImageInfosUI()
    window.show()
    sys.exit(app.exec_())
