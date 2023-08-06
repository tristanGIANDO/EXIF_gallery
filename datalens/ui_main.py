import sys, webbrowser
from PyQt5 import QtWidgets,QtCore, QtGui
import __infos__, envs

from api.database import Database
from ui_astrophoto import AstroWorkspaceTree, AstroListWidget
from ui_image import ImageInfosUI
   
class MainUI( QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("%s v-%s"%(__infos__.__title__,
                                       __infos__.__version__))
        self.resize(1900, 800)

        self._current_view = "grid"

        self.create_widgets()
        self.create_actions()
        self.create_layouts()
        self.create_connections()

        self._db = Database()
        
        self._update()

    def create_widgets(self):
        # tree
        if self._current_view == "grid":
            self.tree = AstroWorkspaceTree()
        else:
            self.card_wdg = AstroListWidget()

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
        
        self.grid_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["full"]), 
            "Grid View", 
            self)
        
        self.card_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["add_file"]), 
            "Card View", 
            self)
        
        self.web_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["full"]), 
            "Website", 
            self)

    def create_layouts(self):
        # toolbar
        self.toolbar = QtWidgets.QToolBar(self)
        self.toolbar.setIconSize(QtCore.QSize(30,30))
        self.addToolBar(self.toolbar)

        self.toolbar.addAction(self.add_files_action)
        self.toolbar.addAction(self.remove_files_action)
        self.toolbar.addAction(self.reload_files_action)
        self.toolbar.addAction(self.web_action)

        # toolbar
        # self.b_toolbar = QtWidgets.QToolBar(self)
        # self.b_toolbar.setIconSize(QtCore.QSize(30,30))
        # self.addToolBar(self.b_toolbar)

        # self.b_toolbar.addAction(self.grid_action)
        # self.b_toolbar.addAction(self.card_action)

        # main self.central_layout
        self.central_layout = QtWidgets.QVBoxLayout()
        if self._current_view == "grid":
            self.central_layout.addWidget(self.tree)
        else:
            self.central_layout.addWidget(self.card_wdg)
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(self.central_layout)
        self.setCentralWidget(central_widget)

    def create_connections(self):
        if self._current_view == "grid":
            self.tree.itemChanged.connect(self.on_item_changed)

        self.add_files_action.triggered.connect(self.on_add_files_clicked)
        self.remove_files_action.triggered.connect(self.on_remove_files_clicked)
        self.reload_files_action.triggered.connect(self._update)
        self.grid_action.triggered.connect(self.on_grid_clicked)
        self.card_action.triggered.connect(self.on_card_clicked)
        self.web_action.triggered.connect(self.on_web_triggered)

    def _update(self):
        if self._current_view == "grid":
            self.tree.blockSignals(True)
            self.tree.clear()
            for file_data in self._db._files.select_rows():
                self.tree.add_item(file_data)
            self.tree.blockSignals(False)
        else:
            self.card_wdg.clear()
            for file_data in self._db._files.select_rows():
                self.card_wdg.add_item(file_data)
        
    def open_image_info(self):
        ui = ImageInfosUI()
        if ui.exec_():
            data = ui.read()
            self._db._files.insert_into(data)
            self._update()

    def on_add_files_clicked(self):
        self.open_image_info()

    def on_remove_files_clicked(self):
        item = self.tree.remove_tree_item()
        if not item:
            return
        self._db._files.delete_from(item.text(0),
                                    item.text(1))

    def on_item_changed(self, item, column):
        self.tree.update_item(self._db, item, column)

    def on_grid_clicked(self):
        self.set_grid_view()
    
    def set_grid_view(self):
        self.central_layout.removeWidget(self.card_wdg)
        self.tree = AstroWorkspaceTree()
        self.central_layout.addWidget(self.tree)
        self._current_view = "grid"
        self._update()
    
    def on_card_clicked(self):
        self.set_card_view()
    
    def set_card_view(self):
        self.central_layout.removeWidget(self.tree)

        self.card_wdg = AstroListWidget()
        self.central_layout.addWidget(self.card_wdg)
        self._current_view = "card"
        self._update()

    def on_web_triggered(self):
        webbrowser.open(r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\datalens\index.html")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())