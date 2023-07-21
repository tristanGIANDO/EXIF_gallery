import os, sys
from PyQt5 import QtWidgets,QtCore
import __infos__

from api.file import File

IDX_IMAGE = 0
IDX_NAME = 1
IDX_PATH = 2
NB_SECTIONS = 3

class FileItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, file, *args, **kwargs):
        
        self._file = file
      
        headers = [
            file.get_name(),
            file.get_source()
        ]

        super(FileItem, self).__init__(headers, *args, **kwargs)

class MainUI( QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("%s v-%s"%(__infos__.__title__,__infos__.__version__))
        self.resize(700, 400)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        # tree
        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setColumnCount(NB_SECTIONS)
        self.tree.setHeaderLabels(["Scene Name",
                                   "Path"])
        self.tree.setRootIsDecorated(False)
        self.tree.setSortingEnabled(True)
        self.tree.header().sectionsMovable()
      
        self.tree.header().setSectionResizeMode(IDX_IMAGE, QtWidgets.QHeaderView.ResizeToContents)

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

    def add_tree_item(self, IDX_PATH):
        # create object
        file = File(IDX_PATH)

        # item
        item = FileItem(file)
        self.tree.addTopLevelItem(item)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())