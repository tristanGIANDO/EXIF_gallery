import typing
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget
from datalens.ui_image import ImageInfosUI
from datalens.api import envs

class WorkspaceTree( QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()

        self.setRootIsDecorated(False)
        self.setSortingEnabled(True)
        self.header().sectionsMovable()
 
        self.header().setSectionHidden(0, True) # ID
        self.header().setSectionHidden(1, True) # Path

    def remove_tree_item(self):
        selected_items = self.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            parent = item.parent()
            if parent is None:
                index = self.indexOfTopLevelItem(item)
                self.takeTopLevelItem(index)
            else:
                parent.removeChild(item)
        return item

class CreateAlbumUI(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Album")
        self.resize(300, 70)

        main_layout = QtWidgets.QVBoxLayout(self)
        font_bold = QtGui.QFont("Arial", 8, QtGui.QFont.Bold)
        album_name_lbl = QtWidgets.QLabel("Name")
        album_name_lbl.setFont(font_bold)
        self.album_name_le = QtWidgets.QLineEdit()
        self.album_name_le.setPlaceholderText("eg: Trip to Norway 2023")

        album_type_lbl = QtWidgets.QLabel("Type")
        album_type_lbl.setFont(font_bold)
        self.album_type_cb = QtWidgets.QComboBox()
        self.album_type_cb.addItems(["Astro",
                                     "Landscape",
                                     "People",
                                     "Studio",
                                     "Urban",
                                     "Wild Life"])
        
        grid_layout = QtWidgets.QGridLayout()
        pos = 0
        for label, wdg in zip([album_name_lbl, album_type_lbl],
                              [self.album_name_le, self.album_type_cb]):
            grid_layout.addWidget(label, 0, pos)
            grid_layout.addWidget(wdg, 1, pos)
            pos += 1
        main_layout.addLayout(grid_layout)

        buttons_layout = QtWidgets.QHBoxLayout()
        self.ok_btn = QtWidgets.QPushButton("Create Album")
        self.ok_btn.clicked.connect(self._accept)
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.deleteLater)
        buttons_layout.addWidget(self.ok_btn)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addStretch(1)

        main_layout.addLayout(buttons_layout)

    def _accept(self):
        self.deleteLater()
        self.accept()

    def read(self):
        return {
            envs.ALBUM_NAME : self.album_name_le.text(),
            envs.ALBUM_TYPE : self.album_type_cb.currentText()
        }
    
class ActionButton(QtWidgets.QPushButton):
    def __init__(self, action, parent=None):
        super().__init__(parent)
        self.setText(action.text())
        self.setIcon(action.icon())
        self.setIconSize(QtCore.QSize(60,60))
        self.setFixedSize(QtCore.QSize(300,70))
        self.clicked.connect(action.trigger)

class SpinWdg(QtWidgets.QWidget):
    def __init__(self, item, column, value, mode = "simple", parent=None) -> None:
        super().__init__(parent)
        self.item = item
        self.column = column
        self.mode = mode
        self.setLayout(QtWidgets.QVBoxLayout())
        if mode == "simple":
            self.box = QtWidgets.QSpinBox()
        elif mode == "date":
            self.box = QtWidgets.QDateEdit()
            self.box.setDisplayFormat("yyyy, MM, dd")
        else:
            self.box = QtWidgets.QDoubleSpinBox()
        # self.box.setFixedWidth(60)
        if mode == "date":
            print(value)
            date = [int(d) for d in value.split(",")]
            q_date = QtCore.QDate(date[0], date[1], date[2])
            self.box.setDate(q_date)  
        else:
            self.box.setMaximum(99999)
            self.box.setValue(value)
        self.layout().addWidget(self.box)

        if mode == "date":
            self.box.dateChanged.connect(self.setItemText)
        else:
            self.box.valueChanged.connect(self.setItemText)
    
    def setItemText(self):
        if self.mode == "date":
            value = self.box.text()
        else:
            value = str(self.box.value())
        if not value:
            return
        self.item.setText(self.column, value)

class ComboBoxWdg(QtWidgets.QWidget):
    def __init__(self, item, column, values) -> None:
        super().__init__()
        self.item = item
        self.column = column
        self.setLayout(QtWidgets.QVBoxLayout())
        self.box = QtWidgets.QComboBox()

        for v in values:
            self.box.addItem(v)
        self.box.setCurrentText(self.item.text(self.column))
        self.layout().addWidget(self.box)

        self.box.currentTextChanged.connect(self.setItemText)
    
    def setItemText(self):
        value = str(self.box.currentText())
        if not value:
            return
        self.item.setText(self.column, value)