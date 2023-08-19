import sys, webbrowser
from PyQt5 import QtWidgets,QtCore, QtGui
import __infos__, envs

from api.database import Database
from api import api_utils
from ui_astrophoto import AstroWorkspaceTree, AstroListWidget
from ui_image import ImageInfosUI, ImageViewerUI
from ui_user import UserInfosUI
import os
   
class MainUI( QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("%s v-%s"%(__infos__.__title__,
                                       __infos__.__version__))
        self.resize(1800, 800)

        self.create_widgets()
        self.create_actions()
        self.create_layouts()
        self.create_connections()

        self._db = Database()
        
        self.list_wdg.setVisible(False)
        self._update()

    def create_widgets(self):
        self.tree = AstroWorkspaceTree()
        self.list_wdg = AstroListWidget()

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
        
        self.view_mode_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["card"]), 
            "Change View Mode", 
            self)
        
        self.viewer_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["viewer"]), 
            "Image viewer", 
            self)
        
        self.web_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["website"]), 
            "Website", 
            self)
        
        self.user_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["user"]), 
            "About you", 
            self)

    def create_layouts(self):
        # toolbar
        self.image_toolbar = QtWidgets.QToolBar(self)
        self.image_toolbar.setIconSize(QtCore.QSize(30,30))
        self.addToolBar(self.image_toolbar)
        self.image_toolbar.addAction(self.reload_files_action)
        self.image_toolbar.addAction(self.add_files_action)
        self.image_toolbar.addAction(self.remove_files_action)
        self.image_toolbar.addAction(self.viewer_action)

        # toolbar
        self.view_toolbar = QtWidgets.QToolBar(self)
        self.view_toolbar.setIconSize(QtCore.QSize(30,30))
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.view_toolbar)
        self.view_toolbar.addAction(self.view_mode_action)
        self.view_toolbar.addAction("Created by Tristan Giandoriggio")
        
        # toolbar
        self.user_toolbar = QtWidgets.QToolBar(self)
        self.user_toolbar.setIconSize(QtCore.QSize(30,30))
        self.addToolBar(self.user_toolbar)
        self.user_toolbar.addAction(self.user_action)
        self.user_toolbar.addAction(self.web_action)

        # main self.central_layout
        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_layout.addWidget(self.tree)
        self.central_layout.addWidget(self.list_wdg)
        central_widget = QtWidgets.QWidget(self)
        central_widget.setLayout(self.central_layout)
        self.setCentralWidget(central_widget)

    def create_connections(self):
        self.tree.itemChanged.connect(self.on_item_changed)

        self.add_files_action.triggered.connect(self.on_add_files_clicked)
        self.remove_files_action.triggered.connect(self.on_remove_files_clicked)
        self.reload_files_action.triggered.connect(self._update)
        self.view_mode_action.triggered.connect(self.on_view_triggered)
        self.viewer_action.triggered.connect(self.on_viewer_triggered)
        self.web_action.triggered.connect(self.on_web_triggered)
        self.user_action.triggered.connect(self.on_user_triggered)

    def _update(self):
        self.tree.blockSignals(True)
        self.tree.clear()
        for file_data in self._db._files.select_rows():
            self.tree.add_item(file_data)
        self.tree.blockSignals(False)
        
        self.list_wdg.clear()
        for file_data in self._db._files.select_rows():
            self.list_wdg.add_item(file_data)
        
    def open_image_info(self):
        ui = ImageInfosUI()
        if ui.exec_():
            data = ui.read()
            self._db._files.insert_into(data)
            self._update()
    
    def open_user_info(self):
        user = self._db._you.get_user()
        ui = UserInfosUI(user=user[0])
        if ui.exec_():
            data = ui.read()
            if user:
                self._db._you.update("first_name", data.get("first_name"))
                self._db._you.update("last_name", data.get("last_name"))
                self._db._you.update("description", data.get("description"))
            else:
                self._db._you.insert_into(data)

    def on_add_files_clicked(self):
        self.open_image_info()

    def on_user_triggered(self):
        self.open_user_info()

    def on_remove_files_clicked(self):
        item = self.tree.remove_tree_item()
        if not item:
            return
        self._db._files.delete_from(item.text(0),
                                    item.text(1))

    def on_item_changed(self, item, column):
        self.tree.update_item(self._db, item, column)

    def on_view_triggered(self):
        self.set_view()
    
    def set_view(self):
        if self.tree.isHidden():
            self.list_wdg.setVisible(False)
            self.tree.setVisible(True)
            self.view_mode_action.setIcon(QtGui.QIcon(envs.ICONS["card"]))
        else:
            self.list_wdg.setVisible(True)
            self.tree.setVisible(False)
            self.view_mode_action.setIcon(QtGui.QIcon(envs.ICONS["list"]))

    def on_viewer_triggered(self):
        paths = []
        for file_data in self._db._files.select_rows():
            paths.append(file_data[1])
        ui = ImageViewerUI(paths)
        ui.exec_()

    def on_web_triggered(self):
        paths = []
        for file_data in self._db._files.select_rows():
            paths.append(file_data[1])

        user = self._db._you.get_user()
        if user:
            user_name = f"{user[0][1]} {user[0][2]}"
            user_description = user[0][3]
        html_file = api_utils.create_website(paths, os.path.dirname(__file__),
                    user_name=user_name, user_description=user_description)
        webbrowser.open(html_file)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())