import os, sys
from PyQt5 import QtWidgets,QtCore, QtGui
import __infos__, envs

from api_sql.db import Database
from api.exif_file import ExifFile
from ws_astro_ui import AstroWorkspaceTree, AstroFileItem
   
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
        self.tree = AstroWorkspaceTree()

    def create_layouts(self):
        # toolbar
        self.toolbar = QtWidgets.QToolBar(self)
        self.toolbar.setIconSize(QtCore.QSize(30,30))
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
            self.tree.add_tree_item(file_row)

    def open_file_dialog(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            for path in file_dialog.selectedFiles():
                self.create_file(path)
                self._update()

    def create_file(self, path):
        exif_file = ExifFile(path)
        data = {"name" : exif_file.get_name(),
                "path" : exif_file.get_path(),
                "author" : exif_file.get_author(),
                "comment" : exif_file.get_comment(),
                "id" : exif_file.get_id()
        }
        self._db.add(data)

    def on_add_files_clicked(self):
        self.open_file_dialog()

    def on_remove_files_clicked(self):
        item = self.tree.remove_tree_item()
        if not item:
            return
        self._db.remove_file(item.text(0),
                             item.text(1))

    def on_item_changed(self, item, column):
        self.tree.update_item(self._db, item, column)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())