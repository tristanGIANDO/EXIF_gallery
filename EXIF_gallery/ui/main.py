import sys, webbrowser
from PyQt5 import QtWidgets,QtCore, QtGui
from EXIF_gallery import __infos__
from EXIF_gallery.api.database import Database
from EXIF_gallery.api import envs as api_envs
from EXIF_gallery.ui.astrophoto import AstroWorkspaceTree, AstroImageInfosUI
from EXIF_gallery.ui.image import ImageViewerUI
from EXIF_gallery.ui.user import UserInfosUI
from EXIF_gallery.ui.utils import CreateAlbumUI, ActionButton, ListWidget
from EXIF_gallery.ui.features import create_website, GraphUI
from EXIF_gallery.ui import envs

class MainUI( QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("%s v-%s"%(__infos__.__title__,
                                       __infos__.__version__))
        self.setWindowIcon(envs.ICONS.get("logo"))
        self.resize(1850, 800)

        self._db = Database()
        self._current_album = ""
        
        self.create_widgets()
        self.create_actions()
        self.create_layouts()
        self.create_connections()
    
        self._update_albums()
        self._update_user()

        self.set_view()

    def create_widgets(self):
        self.title = QtWidgets.QLabel("EXIF_gallery")
        self.title.setFont(QtGui.QFont("Impact", 16))
        self.list_wdg = ListWidget(self._db)
        self.albums_cb = QtWidgets.QComboBox()
        self.albums_cb.setFixedSize(200,40)
        self.albums_cb.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        self.tree = AstroWorkspaceTree(self._db)

    def create_actions(self):
        self.add_files_action = QtWidgets.QAction(envs.ICONS.get("add_file"), "Add File", self)
        
        self.remove_files_action = QtWidgets.QAction(
             envs.ICONS.get("remove_file"), "Remove File", self)
        
        self.reload_files_action = QtWidgets.QAction(
             envs.ICONS.get("reload"), "Reload", self)
        
        self.view_mode_action = QtWidgets.QAction(
             envs.ICONS.get("card"), "Large Icons / Content", self)

        self.viewer_action = QtWidgets.QAction(
             envs.ICONS.get("viewer"), "Image Viewer", self)
        
        self.web_action = QtWidgets.QAction(
             envs.ICONS.get("website"), "Website", self)
        
        self.user_action = QtWidgets.QAction(
             envs.ICONS.get("user"), "About you", self)
        
        self.create_album_action = QtWidgets.QAction(
             envs.ICONS.get("add_album"), "Create Album", self)
        
        self.delete_album_action = QtWidgets.QAction(
             envs.ICONS.get("remove_album"), "Delete Album", self)
        
        self.graph_action = QtWidgets.QAction(
             envs.ICONS.get("graph"), "Show Graph", self)
        
        self.image_size_action = QtWidgets.QAction(
             envs.ICONS.get("list"), "Details", self)
        
        
        self.create_album_btn = ActionButton(self.create_album_action)
        self.add_files_btn = ActionButton(self.add_files_action)

    def create_layouts(self):
        # menu bar
        self.menu_bar = QtWidgets.QMenuBar()
        self.setMenuBar(self.menu_bar)
        self.view_menu = QtWidgets.QMenu("View")
        self.menu_bar.addMenu(self.view_menu)
        self.view_menu.addAction(self.view_mode_action)
        self.view_menu.addAction(self.image_size_action)
        self.help_menu = QtWidgets.QMenu("Help")
        self.menu_bar.addMenu(self.help_menu)
        self.help_menu.addAction("About")
        self.help_menu.addAction("Documentation")

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
        self.album_toolbar.addAction(self.reload_files_action)
        self.album_toolbar.addAction(self.create_album_action)
        self.album_toolbar.addAction(self.delete_album_action)
        self.album_toolbar.addWidget(self.albums_cb)

        # image toolbar
        self.image_toolbar = QtWidgets.QToolBar(self)
        self.image_toolbar.setIconSize(QtCore.QSize(35,35))
        self.image_toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.addToolBar(self.image_toolbar)
        self.image_toolbar.addAction(self.add_files_action)
        self.image_toolbar.addAction(self.remove_files_action)
        self.image_toolbar.addSeparator()
        self.image_toolbar.addAction(self.viewer_action)
        self.image_toolbar.addAction(self.web_action)
        self.image_toolbar.addAction(self.graph_action)

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
        self.central_layout.addWidget(self.create_album_btn)
        self.central_layout.addWidget(self.add_files_btn)
        self.central_layout.setAlignment(QtCore.Qt.AlignCenter)
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
        self.graph_action.triggered.connect(self.on_graph_triggered)
        self.albums_cb.currentTextChanged.connect(self.on_album_changed)
        self.image_size_action.triggered.connect(self.on_image_size_triggered)

    def _update_albums(self, album_name = None):
        self.albums_cb.clear()
        self.albums_cb.blockSignals(True)
        name = ""
        for album_data in self._db._albums.select_rows() or ():
            if len(album_data) >= 2:
                name = album_data[1]
            self.albums_cb.addItem(name)
    
        self._current_album = name
        self.albums_cb.blockSignals(False)
        self.albums_cb.setCurrentText(name)
        self._update_files()
        
    def _update_files(self):
        self.tree.blockSignals(True)
        self.tree.clear()
        self.list_wdg.clear()

        for file in self.get_album_files():
            self.list_wdg.add_item(file)
            self.tree.add_item(file[0])

        self.tree.blockSignals(False)
        self.set_view()
        
    def _update_user(self):
        user = self._db._you.get_user()
        if user:
            try:
                self.user_action.setIcon( QtGui.QIcon(user[4]))
            except:
                self.user_action.setIcon( envs.ICONS.get("logo"))

    def get_album_files(self, album = None):
        if not album:
            album = self._current_album

        return [f for f in self._db._files.select_rows() if f[3] == album]
 
    def open_image_info(self):
        user = self._db._you.get_user()
        if user:
            author = f"{user[1]} {user[2]}"
        else:
            author = None

        ui = AstroImageInfosUI(author)
        if ui.exec_():
            data = ui.read()
            data["album"] = self._current_album
            self._db._files.insert_into(data)
            self._update_albums()
    
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
        self.tree.update_item(item, column)

    def on_view_triggered(self):
        self.set_view()
    
    def set_view(self):
        if self._current_album:
            if self.get_album_files():
                for action in [self.delete_album_action,
                           self.albums_cb,
                            self.viewer_action,
                            self.add_files_action,
                            self.remove_files_action,
                            self.view_mode_action,
                            self.graph_action,
                            self.web_action]:
                    action.setEnabled(True)

                if self.tree.isHidden():
                    self.tree.setVisible(True)
                    self.list_wdg.setVisible(False)
                    self.view_mode_action.setIcon(envs.ICONS.get("card"))
                else:
                    self.tree.setVisible(False)
                    self.list_wdg.setVisible(True)
                    self.view_mode_action.setIcon(envs.ICONS.get("list"))

                self.create_album_btn.setVisible(False)
                self.add_files_btn.setVisible(False)
            else:
                for action in [self.delete_album_action,
                            self.albums_cb,
                            self.add_files_action]:
                    action.setEnabled(True)

                for action in [
                            self.viewer_action,
                            self.remove_files_action,
                            self.view_mode_action,
                            self.graph_action,
                            self.web_action]:
                    action.setEnabled(False)

                self.tree.setVisible(False)
                self.list_wdg.setVisible(False)

                self.create_album_btn.setVisible(False)
                self.add_files_btn.setVisible(True)
        else:
            for action in [self.delete_album_action,
                           self.albums_cb,
                            self.viewer_action,
                            self.add_files_action,
                            self.remove_files_action,
                            self.view_mode_action,
                            self.graph_action,
                            self.web_action]:
                    action.setEnabled(False)

            self.tree.setVisible(False)
            self.list_wdg.setVisible(False)

            self.create_album_btn.setVisible(True)
            self.add_files_btn.setVisible(False)
                    
    def on_viewer_triggered(self):
        paths = []
        for file_data in self.get_album_files():
            paths.append(file_data[1])
        ui = ImageViewerUI(paths)
        ui.showFullScreen()
        ui.exec_()

    def on_graph_triggered(self):
        ui = GraphUI(self._db, self._db._files.select_rows())
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

        html_file = create_website(paths, api_envs.ROOT,
                    user=user, overlays=overlays, albums=albums)
            
        webbrowser.open(html_file)

    def on_create_album_triggered(self):
        ui = CreateAlbumUI()
        if ui.exec_():
            data = ui.read()
            if not data.get("name"):
                message_box = QtWidgets.QMessageBox.critical(
                self,
                "Name error", 
                f"You need to specify a name.",
                QtWidgets.QMessageBox.Ok)
                return
            self._db._albums.insert_into(data)
            self._update_albums(data.get("name"))

    def on_album_changed(self):
        self._current_album = self.albums_cb.currentText()
        print(self._current_album)
        self._update_files()
        self.set_view()
    
    def on_delete_album_triggered(self):
        album_name = self.albums_cb.currentText()
        message_box = QtWidgets.QMessageBox.warning(
            self,
            "Delete Album", 
            f"You are about to delete '{album_name}'.\nThis is irreversible!",
            QtWidgets.QMessageBox.Ok | 
            QtWidgets.QMessageBox.Cancel)
        if message_box == QtWidgets.QMessageBox.Cancel:
            return
        self._db._albums.delete_album(album_name)
        self._update_albums()

    def on_image_size_triggered(self):
        for item in self.tree.get_items():
            try:
                item._update((100,66))
            except:
                pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(open(r"EXIF_gallery\ui\styles\lightstyle.qss").read())

    ui = MainUI()
    ui.show()
    sys.exit(app.exec_())