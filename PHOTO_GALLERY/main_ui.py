import os, sys
from PyQt5 import QtWidgets,QtCore, QtGui
import __infos__

from api.file import File

I_IMAGE = "Image"
I_NAME = "Name"
I_PATH = "Path"
I_CAMERA = "Camera"
I_AUTHOR = "Author"
I_COMMENT = "Comment"

HEADERS = [I_IMAGE, I_NAME, I_PATH, I_CAMERA, I_AUTHOR, I_COMMENT]
NB_SECTIONS = len(HEADERS)

class FileItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, file, *args, **kwargs):
        
        self._file = file
        file_path = file.get_source()
        headers = [
            "",
            file.get_name(),
            file_path,
            "",
            file.get_author_from_data(),
            file.get_comment_from_data()
        ]

        super(FileItem, self).__init__(headers, *args, **kwargs)

class MainUI( QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("%s v-%s"%(__infos__.__title__,__infos__.__version__))
        self.resize(1400, 900)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # tree
        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setColumnCount(NB_SECTIONS)
        self.tree.setHeaderLabels(HEADERS)
        self.tree.setRootIsDecorated(False)
        self.tree.setSortingEnabled(True)
        self.tree.header().sectionsMovable()
        self.tree.header().setSectionResizeMode(HEADERS.index(I_IMAGE), QtWidgets.QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(HEADERS.index(I_NAME), QtWidgets.QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(HEADERS.index(I_AUTHOR), QtWidgets.QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(HEADERS.index(I_COMMENT), QtWidgets.QHeaderView.ResizeToContents)

    def create_layouts(self):
        # toolbar
        self.toolbar = QtWidgets.QToolBar(self)
        self.addToolBar(self.toolbar)

        self.add_files_action = QtWidgets.QAction("Add Files", self)
        self.toolbar.addAction(self.add_files_action)

        self.remove_files_action = QtWidgets.QAction("Remove Files", self)
        self.toolbar.addAction(self.remove_files_action)

        # main layout
        layout = QtWidgets.QVBoxLayout()
        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addWidget(self.tree)
        layout.addLayout(h_layout)
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_connections(self):
        self.add_files_action.triggered.connect(self.on_add_files_clicked)
        self.remove_files_action.triggered.connect(self.on_remove_files_clicked)

    def add_tree_item(self, image_path):
        # create object
        file = File(image_path)

        # item
        item = FileItem(file)
        thumbnail = ImageThumbnail(image_path)

        self.tree.addTopLevelItem(item)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.tree.setItemWidget(item, HEADERS.index(I_IMAGE), thumbnail)

    def remove_tree_item(self):
        selected_items = self.tree.selectedItems()
        for item in selected_items:
            parent = item.parent()
            if parent is None:
                index = self.tree.indexOfTopLevelItem(item)
                self.tree.takeTopLevelItem(index)
            else:
                parent.removeChild(item)

    def open_file_dialog(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            for IDX_PATH in file_dialog.selectedFiles():
                self.add_tree_item(IDX_PATH)

    def on_add_files_clicked(self):
        self.open_file_dialog()

    def on_remove_files_clicked(self):
        self.remove_tree_item()

class ImageThumbnail(QtWidgets.QLabel):
    def __init__(self, image, *args, **kwargs):
        super(ImageThumbnail, self).__init__(*args, **kwargs)
        size = (300,300)
        self.setFixedSize(size[0], size[1])
        self.setAlignment(QtCore.Qt.AlignCenter)
       
        if isinstance(image, str) and os.path.isfile(image):
            image = QtGui.QImage(image)
            pixmap = QtGui.QPixmap(image)

        else:
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(image)
            
        if not pixmap.isNull():
            pixmap = pixmap.scaled(self.width()-5, 
                                   self.height()-5, 
                                   QtCore.Qt.KeepAspectRatio, 
                                   QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())