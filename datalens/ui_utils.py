from PyQt5 import QtWidgets, QtCore, QtGui
from pathlib import Path
from datalens.ui_image import ImageInfosUI

class WorkspaceTree( QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setRootIsDecorated(False)
        self.setSortingEnabled(True)
        self.header().sectionsMovable()
 
        self.header().setSectionHidden(0, True) # ID
        self.header().setSectionHidden(1, True) # Path

    def remove_tree_item(self):
        selected_items = self.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            parent = item.parent()
            if parent is None:
                index = self.indexOfTopLevelItem(item)
                self.takeTopLevelItem(index)
            else:
                parent.removeChild(item)
        return item
    
class ImageViewWidget(QtWidgets.QPushButton):
    def __init__(self, path, size=(300,200)):
        super().__init__()

        self.path = path

        self.setFixedSize(size[0],size[1])

        layout = QtWidgets.QVBoxLayout()

        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.image_label)

        self.load_image(path)

        self.setLayout(layout)

        self.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        ui = ImageInfosUI(self.path)
        ui.exec_()

    def load_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        if not pixmap.isNull():
            aspect_ratio = pixmap.width() / pixmap.height()
            self.image_label.setPixmap(pixmap.scaledToHeight(self.height(), mode=QtCore.Qt.SmoothTransformation))
        else:
            self.image_label.setText("Failed to load image")