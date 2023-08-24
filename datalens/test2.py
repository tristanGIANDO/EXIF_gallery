import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QStackedLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class StackedImageWithButton(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Stacked Image with Button')

        # Création des widgets
        label = QLabel(self)
        pixmap = QPixmap(r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\datalens\icons\list.png")  # Remplacez par le chemin de votre image
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)  # Centrer l'image dans le label

        button = QPushButton('Button')
        button.setMaximumSize(40,40)

        # Création du QStackedLayout
        stacked_layout = QStackedLayout()
        stacked_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        stacked_layout.addWidget(label)
        stacked_layout.addWidget(button)
        
        

        # Appliquer le QStackedLayout au widget principal
        self.setLayout(stacked_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StackedImageWithButton()
    window.show()
    sys.exit(app.exec_())
