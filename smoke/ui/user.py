from PyQt5 import QtWidgets, QtGui, QtCore

from smoke.ui import envs
from smoke.api import envs as api_envs

class UserInfosUI(QtWidgets.QDialog):
    def __init__(self, user=None):
        super().__init__()
    
        self.setWindowTitle("About you")
        self.resize(300, 300)
        self.setWindowIcon(envs.ICONS.get("logo"))
        self.create_widgets()
        self.create_layouts()

        if user:
            self.first_name_le.setText(user[1])
            self.last_name_le.setText(user[2])
            self.description_le.setPlainText(user[3])
            self._path = user[4]
        else:
            self._path = ""

        self._update()

    def create_widgets(self):
        self.first_name_le = QtWidgets.QLineEdit()
        self.last_name_le = QtWidgets.QLineEdit()
        self.description_le = QtWidgets.QPlainTextEdit()
        
        # image
        self.image_lbl = QtWidgets.QWidget()
        self.thumbnail_btn = QtWidgets.QPushButton("Add Thumbnail")
        self.thumbnail_btn.clicked.connect(self.on_thumbnail_clicked)

        # buttons
        self.ok_btn = QtWidgets.QPushButton("OK")
        self.ok_btn.clicked.connect(self._accept)
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.deleteLater)
        
    def create_layouts(self):
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)

        self.image_layout = QtWidgets.QVBoxLayout()
        self.image_layout.addWidget(self.thumbnail_btn)
        self.image_layout.addWidget(self.image_lbl)
        main_layout.addLayout(self.image_layout)

        # Labels
        first_name_lbl = QtWidgets.QLabel("First Name")
        last_name_lbl = QtWidgets.QLabel("Last Name")
        desc_lbl = QtWidgets.QLabel(envs.G_DESC)
        
        font_bold = QtGui.QFont("Arial", 8, QtGui.QFont.Bold)
        for column_lbl in [first_name_lbl, last_name_lbl, desc_lbl]:
            column_lbl.setFont(font_bold)

        # global grid
        global_gb = QtWidgets.QGroupBox()
        grid_layout = QtWidgets.QGridLayout(global_gb)
        
        pos = 0
        for label, wdg in zip([first_name_lbl, last_name_lbl, desc_lbl],
                              [self.first_name_le, self.last_name_le, self.description_le]):
            grid_layout.addWidget(label, pos, 0)
            grid_layout.addWidget(wdg, pos, 1)
            pos += 1
 
        main_layout.addWidget(global_gb)

        # Buttons
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.ok_btn)
        h_layout.addWidget(self.cancel_btn)
        h_layout.addStretch(1)
        main_layout.addLayout(h_layout)

    def _accept(self):
        self.deleteLater()
        self.accept()

    def _update(self):
        if self._path:
            self.image_layout.removeWidget(self.image_lbl)
            self.image_lbl = QtWidgets.QLabel()
            self.image_lbl.setAlignment(QtCore.Qt.AlignCenter)
            pixmap = QtGui.QPixmap(self._path)
            pixmap = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
            self.image_lbl.setPixmap(pixmap)
            self.image_layout.addWidget(self.image_lbl)
            self.thumbnail_btn.setText("Modify Thumbnail")
        
    def read(self):
        return {
                api_envs.FIRST_NAME : self.first_name_le.text(),
                api_envs.LAST_NAME : self.last_name_le.text(),
                api_envs.DESC : self.description_le.toPlainText(),
                api_envs.PATH : self._path
                }
    
    def open_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.gif *.bmp);;All Files (*)", options=options)

        if file_name:
            return file_name
        else:
            return ""
        
    def on_thumbnail_clicked(self):
        self._path = self.open_file_dialog()
        self._update()