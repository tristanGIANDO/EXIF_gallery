import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from datalens import envs

class ImageViewer(QtWidgets.QDialog):
    def __init__(self, paths):
        super().__init__()
        if not paths:
            return
        
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 900, 700)

        self.central_widget = QtWidgets.QWidget(self)

        self.layout = QtWidgets.QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.prev_button = QtWidgets.QPushButton(QtGui.QIcon(envs.ICONS["previous"]), "")
        self.prev_button.setFixedSize(40,40)
        self.prev_button.setIconSize(QtCore.QSize(35,35))
        self.prev_button.clicked.connect(self.show_previous_image)
        self.layout.addWidget(self.prev_button)

        self.image_label = QtWidgets.QLabel(self)
        self.layout.addWidget(self.image_label)

        self.next_button = QtWidgets.QPushButton(QtGui.QIcon(envs.ICONS["next"]), "")
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
            pixmap = pixmap.scaled(900, 600, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

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

if __name__ == "__main__":
    paths = [r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\datalens\icons\0.png",
             r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\datalens\icons\1.png",
             r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\datalens\icons\2.png",
             r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\datalens\icons\3.png"
             ]
    app = QtWidgets.QApplication(sys.argv)
    viewer = ImageViewer(paths)
    viewer.show()
    sys.exit(app.exec_())
