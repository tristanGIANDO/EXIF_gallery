import os, sys
from PyQt5 import QtWidgets,QtCore, QtGui
import __infos__, envs

from api_sql.db import Database
from api.exif_file import ExifFile

I_ID = "ID"
I_IMAGE = "Image"
I_NAME = "Name"
I_PATH = "Path"
I_CAMERA = "Camera"
I_ISO = "ISO"
I_EXPOSURE_TIME = "Exposure Time"
I_APERTURE = "Aperture"
I_AUTHOR = "Author"
I_COMMENT = "Comment"

HEADERS = [I_ID, I_IMAGE, I_NAME, I_PATH, I_CAMERA, I_AUTHOR, I_COMMENT]
NB_SECTIONS = len(HEADERS)

class FileItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, data, *args, **kwargs):

        super(FileItem, self).__init__(*args, **kwargs)

        if data:
            print(data)
            self.setText(HEADERS.index(I_ID), str(data[0]))
            self.setText(HEADERS.index(I_NAME), data[1])
            self.setText(HEADERS.index(I_PATH), data[2])
            self.setText(HEADERS.index(I_AUTHOR), data[3])
            self.setText(HEADERS.index(I_COMMENT), data[4])
            
class MainUI( QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("%s v-%s"%(__infos__.__title__,
                                       __infos__.__version__))
        self.resize(1200, 700)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self._db = Database()
        self._update()

    def create_widgets(self):
        # tree
        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setColumnCount(NB_SECTIONS)
        self.tree.setHeaderLabels(HEADERS)
        self.tree.setRootIsDecorated(False)
        self.tree.setSortingEnabled(True)
        self.tree.header().sectionsMovable()
        for header in HEADERS:
            if HEADERS.index(header) == HEADERS.index(I_NAME):
                continue
            self.tree.header().setSectionResizeMode(HEADERS.index(header),
                                    QtWidgets.QHeaderView.ResizeToContents)
        self.tree.header().setSectionHidden(HEADERS.index(I_ID), False)

    def create_layouts(self):
        # toolbar
        self.toolbar = QtWidgets.QToolBar(self)
        self.addToolBar(self.toolbar)

        self.add_files_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["add_file"]), 
            "Add Files", 
            self)
        self.toolbar.addAction(self.add_files_action)

        self.remove_files_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["remove_file"]),
            "Remove Files", 
            self)
        self.toolbar.addAction(self.remove_files_action)

        self.reload_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["reload"]),
            "Reload", 
            self)
        self.toolbar.addAction(self.reload_action)

        # main layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tree)

        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_connections(self):
        self.tree.itemChanged.connect(self.on_item_changed)

        self.add_files_action.triggered.connect(self.on_add_files_clicked)
        self.remove_files_action.triggered.connect(self.on_remove_files_clicked)

    def _update(self):
        self.tree.clear()
        for file_row in self._db.get_rows():
            self.add_tree_item(file_row)

    def add_tree_item(self, file_row):
        item = FileItem(file_row)
        thumbnail = ImageViewWidget(file_row[2])

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
        return item

    def open_file_dialog(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            for path in file_dialog.selectedFiles():
                self.create_file(path)
                self._update()

    def create_file(self, path):
        exif_file = ExifFile(path)
        data = [exif_file.get_name(),
                exif_file.get_path(),
                exif_file.get_author(),
                exif_file.get_comment()
            ]
        self._db.add(data)

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
        item = self.remove_tree_item()
        self._db.remove_file(item.text(HEADERS.index(I_ID)))

    def on_save_btn_clicked(self):
        self.save()

    def on_item_changed(self, item, column):
        pass
        # file = item._file
        # if column == HEADERS.index(I_NAME):
        #     file.set_name(item.text(column))
        
        # elif column == HEADERS.index(I_COMMENT):
        #     file.set_comment(item.text(column))

class ImageViewWidget(QtWidgets.QLabel):
    def __init__(self, image_path, *args, **kwargs):
        super(ImageViewWidget, self).__init__(*args, **kwargs)
        size = (300,200)
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())