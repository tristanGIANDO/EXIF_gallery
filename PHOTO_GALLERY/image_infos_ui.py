import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class ImageInfosUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        main_layout = QtWidgets.QVBoxLayout()

        # Image
        image_label = QtWidgets.QLabel()
        pixmap = QPixmap(r"C:\Users\giand\OneDrive\Images\@PORTFOLIO\america_001.jpg")
        pixmap = pixmap.scaled(690, 600, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        main_layout.addWidget(image_label, alignment=Qt.AlignCenter)

        # Title
        self.title_le = QtWidgets.QLineEdit("NAME")
        title_font = QFont("Arial", 18, QFont.Bold)  # Set font size to 18 and make it bold
        self.title_le.setFont(title_font)
        self.title_le.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title_le, alignment=Qt.AlignCenter)

        # Subtitle
        self.description_le = QtWidgets.QLineEdit("Description")
        self.description_le.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.description_le, alignment=Qt.AlignCenter)

        # EQUIPMENT GroupBox
        equipment_gb = QtWidgets.QGroupBox("Equipment")
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

        # Set the fixed size for the window
        

        self.setLayout(main_layout)
        self.setWindowTitle("PyQt Vertical Interface Example")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ImageInfosUI()
    window.show()
    sys.exit(app.exec_())
