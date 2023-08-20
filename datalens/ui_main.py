import sys, webbrowser, os
from PyQt5 import QtWidgets,QtCore, QtGui
from datalens import __infos__, envs
from datalens.api.database import Database
from datalens.api import envs as api_envs
from datalens.ui_astrophoto import AstroWorkspaceTree, AstroListWidget
from datalens.ui_image import ImageInfosUI, ImageViewerUI
from datalens.ui_user import UserInfosUI
from datalens.ui_utils import CreateAlbumUI
from datalens.web import website
   
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
        self._current_album = ""
        
        self.list_wdg.setVisible(False)
        self._update_albums()
        self._update_files()
        self._update_user()

    def create_widgets(self):
        self.title = QtWidgets.QLabel("DataLens")
        self.title.setFont(QtGui.QFont("Impact", 16))

        self.tree = AstroWorkspaceTree()
        self.list_wdg = AstroListWidget()
        self.albums_cb = QtWidgets.QComboBox()
        self.albums_cb.setFixedSize(200,40)
        self.albums_cb.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))

    def create_actions(self):
        self.add_files_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["add_file"]), "Add File", self)
        
        self.remove_files_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["remove_file"]), "Remove File", self)
        
        self.reload_files_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["reload"]), "Reload", self)
        
        self.view_mode_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["card"]), "Change View Mode", self)
        
        self.viewer_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["viewer"]), "Image Viewer", self)
        
        self.web_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["website"]), "Website", self)
        
        self.user_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["user"]), "About you", self)
        
        self.create_album_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["add_album"]), "Create Album", self)
        
        self.delete_album_action = QtWidgets.QAction(
            QtGui.QIcon(envs.ICONS["remove_album"]), "Delete Album", self)

    def create_layouts(self):

        # user toolbar
        self.user_toolbar = QtWidgets.QToolBar(self)
        self.user_toolbar.setIconSize(QtCore.QSize(60,60))
        self.addToolBar(self.user_toolbar)
        self.user_toolbar.addAction(self.user_action)

        # album toolbar
        self.album_toolbar = QtWidgets.QToolBar(self)
        self.album_toolbar.setIconSize(QtCore.QSize(35,35))
        self.album_toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.addToolBar(self.album_toolbar)
        self.album_toolbar.addAction(self.create_album_action)
        self.album_toolbar.addAction(self.delete_album_action)
        self.album_toolbar.addWidget(self.albums_cb)

        # image toolbar
        self.image_toolbar = QtWidgets.QToolBar(self)
        self.image_toolbar.setIconSize(QtCore.QSize(35,35))
        self.image_toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.addToolBar(self.image_toolbar)
        self.image_toolbar.addAction(self.reload_files_action)
        self.image_toolbar.addAction(self.add_files_action)
        self.image_toolbar.addAction(self.remove_files_action)
        self.image_toolbar.addSeparator()
        self.image_toolbar.addAction(self.viewer_action)
        self.image_toolbar.addAction(self.web_action)

        # view toolbar
        self.view_toolbar = QtWidgets.QToolBar(self)
        self.view_toolbar.setIconSize(QtCore.QSize(35,35))
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.view_toolbar)
        self.view_toolbar.addAction(self.view_mode_action)
        self.view_toolbar.addWidget(self.title)
        self.view_toolbar.addAction("Created by Tristan Giandoriggio")

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
        self.reload_files_action.triggered.connect(self._update_files)
        self.view_mode_action.triggered.connect(self.on_view_triggered)
        self.viewer_action.triggered.connect(self.on_viewer_triggered)
        self.web_action.triggered.connect(self.on_web_triggered)
        self.user_action.triggered.connect(self.on_user_triggered)
        self.create_album_action.triggered.connect(self.on_create_album_triggered)
        self.delete_album_action.triggered.connect(self.on_delete_album_triggered)
        self.albums_cb.currentTextChanged.connect(self.on_album_changed)

    def _update_files(self):
        self.tree.blockSignals(True)
        self.tree.clear()
        self.list_wdg.clear()

        for file in self.get_album_files():
            self.tree.add_item(file)
            self.list_wdg.add_item(file)

        self.tree.blockSignals(False)
        
    def _update_albums(self, album_name = None):
        self.albums_cb.clear()
        name = ""
        for album_data in self._db._albums.select_rows() or ():
            if len(album_data) >= 2:
                name = album_data[1]
            self.albums_cb.addItem(name)
    
        if album_name:
            self._current_album = album_name
        else:
            self._current_album = name
        self.albums_cb.setCurrentText(self._current_album)
        
    def _update_user(self):
        user = self._db._you.get_user()
        if user:
            try:
                self.user_action.setIcon(QtGui.QIcon(user[4]))
            except:
                pass

    def get_album_files(self, album = None):
        if not album:
            album = self._current_album
        return [f for f in self._db._files.select_rows() if f[3] == album]

    def open_image_info(self):
        ui = ImageInfosUI()
        if ui.exec_():
            data = ui.read()
            data["album"] = self._current_album
            self._db._files.insert_into(data)
            self._update_files()
    
    def open_user_info(self):
        user = self._db._you.get_user()
        ui = UserInfosUI(user=user)
        if ui.exec_():
            data = ui.read()
            if user:
                self._db._you.update("first_name", data.get("first_name"))
                self._db._you.update("last_name", data.get("last_name"))
                self._db._you.update("description", data.get("description"))
                self._db._you.update("path", data.get("path"))
            else:
                self._db._you.insert_into(data)
            self._update_user()

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
        for file_data in self.get_album_files():
            paths.append(file_data[1])
        ui = ImageViewerUI(paths)
        ui.exec_()

    def on_web_triggered(self):
        user = self._db._you.get_user()
        albums = []
        for album_data in self._db._albums.select_rows():
            albums.append(album_data[1])
        
        paths = []
        overlays = []
        for file_data in self._db._files.select_rows():
            paths.append(file_data[1])
            overlays.append(file_data[2])

        html_file = website.create_website(paths, api_envs.ROOT,
                    user=user, overlays=overlays, albums=albums)
            
        webbrowser.open(html_file)

    def on_create_album_triggered(self):
        ui = CreateAlbumUI()
        if ui.exec_():
            data = ui.read()
            self._db._albums.insert_into(data)
            self._update_albums(data.get("name"))

    def on_album_changed(self):
        self._current_album = self.albums_cb.currentText()
        self._update_files()
    
    def on_delete_album_triggered(self):
        album_name = self.albums_cb.currentText()
        self._db._albums.delete_album(album_name)
        self._update_albums()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())