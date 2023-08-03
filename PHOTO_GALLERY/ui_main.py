import sys
from PyQt5 import QtWidgets,QtCore, QtGui
import __infos__, envs

from api.database import Database
from ui_astrophoto import AstroWorkspaceTree
from ui_image import ImageInfosUI
   
class MainUI( QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("%s v-%s"%(__infos__.__title__,
                                       __infos__.__version__))
        self.resize(1500, 800)

        self.create_widgets()
        self.create_actions()
        self.create_layouts()
        self.create_connections()

        self._db = Database()
        self._update()

    def create_widgets(self):
        # tree
        self.tree = AstroWorkspaceTree()

    def create_actions(self):
        self.add_files_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["add_file"]), 
            "Add Files", 
            self)
        
        self.remove_files_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["remove_file"]),
            "Remove Files", 
            self)
        
        self.reload_files_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["reload"]),
            "Reload Files", 
            self)

    def create_layouts(self):
        # toolbar
        self.toolbar = QtWidgets.QToolBar(self)
        self.toolbar.setIconSize(QtCore.QSize(30,30))
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.add_files_action)
        self.toolbar.addAction(self.remove_files_action)
        self.toolbar.addAction(self.reload_files_action)

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
        self.reload_files_action.triggered.connect(self._update)

    def _update(self):
        self.tree.clear()
        for file_row in self._db.get_rows():
            self.tree.add_tree_item(file_row)

    def open_file_dialog(self):
        file_dialog = QtWidgets.QFileDialog(self)
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if not file_dialog.exec_():
            return
        path = file_dialog.selectedFiles()[0] # temp
        self.open_image_info(path)
        
    def open_image_info(self, path):
        app = QtWidgets.QApplication(sys.argv)
        window = ImageInfosUI(path)
        window.show()
        data = window.read()
        self._db.add(data)
        self._update()
        sys.exit(app.exec_())

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