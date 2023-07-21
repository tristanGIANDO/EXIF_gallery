import os, sys
from PyQt5 import QtWidgets,QtCore, QtGui
import __infos__

from image.exif_file import ExifFile
from database.database import Database

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
        file_path = file.get_path()
        headers = [
            "",
            file.get_name(),
            file_path,
            "",
            file.get_author(),
            file.get_comment()
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

        database = Database(r"C:\Users\giand\.database.json")
        self._files = database.read()
        self._update()

    def create_widgets(self):
        # tree
        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setColumnCount(NB_SECTIONS)
        self.tree.setHeaderLabels(HEADERS)
        self.tree.setRootIsDecorated(False)
        self.tree.setSortingEnabled(True)
        self.tree.header().sectionsMovable()
        self.tree.header().setSectionResizeMode(HEADERS.index(I_IMAGE),
                                                QtWidgets.QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(HEADERS.index(I_NAME),
                                                QtWidgets.QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(HEADERS.index(I_AUTHOR),
                                                QtWidgets.QHeaderView.ResizeToContents)
        self.tree.header().setSectionResizeMode(HEADERS.index(I_COMMENT),
                                                QtWidgets.QHeaderView.ResizeToContents)

        # button
        self.save_btn = QtWidgets.QPushButton("Save album")

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
        layout.addWidget(self.save_btn)
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_connections(self):
        self.tree.itemChanged.connect(self.on_item_changed)

        self.add_files_action.triggered.connect(self.on_add_files_clicked)
        self.remove_files_action.triggered.connect(self.on_remove_files_clicked)
        self.save_btn.clicked.connect(self.on_save_btn_clicked)

    def _update(self):
        for file in self._files:
            self.add_tree_item(file.get("path",""))

    def add_tree_item(self, image_path):
        # create object
        file = ExifFile(image_path)

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
            for path in file_dialog.selectedFiles():
                self.add_tree_item(path)

    def save(self):
        items = self.tree.findItems(
            "",
            QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive,
            0)
        
        for item in items:
            item._file.save()

    def on_add_files_clicked(self):
        self.open_file_dialog()

    def on_remove_files_clicked(self):
        self.remove_tree_item()

    def on_save_btn_clicked(self):
        self.save()

    def on_item_changed(self, item, column):
        file = item._file
        if column == HEADERS.index(I_NAME):
            file.set_name(item.text(column))
        
        elif column == HEADERS.index(I_COMMENT):
            file.set_comment(item.text(column))

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