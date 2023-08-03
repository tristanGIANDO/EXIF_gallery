from PyQt5 import QtWidgets, QtCore, QtGui

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
    
class ImageViewWidget(QtWidgets.QLabel):
    def __init__(self, image_path, *args, **kwargs):
        super(ImageViewWidget, self).__init__(*args, **kwargs)
        size = (150,100)
        self.setFixedSize(size[0], size[1])
        self.setAlignment(QtCore.Qt.AlignCenter)

        pixmap = QtGui.QPixmap()
        if os.path.isfile(image_path):   
            if isinstance(image_path, str):
                image = QtGui.QImage(image_path)
                pixmap = QtGui.QPixmap(image)
            else:
                pixmap.loadFromData(image_path)
            
        if not pixmap.isNull():
            pixmap = pixmap.scaled(self.width()-2, 
                                   self.height()-2, 
                                   QtCore.Qt.KeepAspectRatio, 
                                   QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)