from PyQt5 import QtWidgets,QtCore, QtGui
from pathlib import Path
from datalens.ui_utils import WorkspaceTree, SpinWdg
from datalens import envs
from datalens.api import envs as api_envs
from datalens.ui_image import ThumbnailButton
import os

HEADERS = [envs.G_ID, envs.G_PATH, envs.G_IMAGE, 
           envs.G_SUBJECT, envs.G_DESC, envs.G_MAKE, envs.G_MODEL,
           envs.A_MOUNT, envs.G_FOCAL, envs.G_F_NUMBER, envs.G_ISO,
           envs.A_LIGHTS, envs.G_EXPOSURE_TIME, envs.A_TOTAL_TIME,
           envs.G_LOCATION, envs.A_BORTLE, envs.A_MOON_PHASE, 
           envs.G_SOFTWARE, envs.G_AUTHOR, envs.G_COMMENT, envs.G_DATE,
           envs.G_PATH_BRUT]
NB_SECTIONS = len(HEADERS)

class AstroFileItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data, *args, **kwargs):

        super(AstroFileItem, self).__init__(*args, **kwargs)
        if not data:
            return
        self._parent = parent
        self._data = data

        self._update()

    def _update(self):
        img_path = Path(self._data[1])
        self.setText(0, self._data[0]) #id
        self.setText(1, str(img_path)) #img_path
        for i in range(2,NB_SECTIONS):
            if i == HEADERS.index(envs.A_MOON_PHASE):
                self.setText(i, envs.MOON_PHASES.get(self._data[i-1]))
            else:
                try:
                    self.setText(i+1, str(self._data[i]))
                except:
                    pass
            if i % 2 == 0:
                self.setBackground(i, QtGui.QColor(240,240,240))
        
        # spinboxes
        focal_box = SpinWdg(int(self._data[HEADERS.index(envs.G_FOCAL)-1]))
        iso_box= SpinWdg(int(self._data[HEADERS.index(envs.G_ISO)-1]))
        f_box = SpinWdg(float(self._data[HEADERS.index(envs.G_F_NUMBER)-1]), mode="double")
        light_box = SpinWdg(int(self._data[HEADERS.index(envs.A_LIGHTS)-1]))
        bortle_box = SpinWdg(int(self._data[HEADERS.index(envs.A_BORTLE)-1]))
        # icons
        self.setIcon(HEADERS.index(envs.A_MOON_PHASE),
                     QtGui.QIcon(envs.ICONS[self._data[15]]))
        
        r = int(self._data[HEADERS.index(envs.G_ISO)-1]/100*3.5)
        if r > 255:
            r = 255
        iso_color = QtGui.QColor(r, 100, 30)
        iso_icon = QtGui.QPixmap(20,20)
        iso_icon.fill(iso_color)
        self.setIcon(HEADERS.index(envs.G_ISO), QtGui.QIcon(iso_icon))
    
        # get small image path
        small_image_path = img_path.parent / (img_path.stem + api_envs.IMAGE_SMALL_SUFFIX + img_path.suffix)
        image_thumbnail = ThumbnailButton(path=str(small_image_path))

        # get small brut path
        small_brut_path = img_path.parent / (img_path.stem + api_envs.BRUT_SMALL_SUFFIX + img_path.suffix)
        if os.path.isfile(small_brut_path):
            brut_thumbnail = ThumbnailButton(path=str(small_brut_path))

        self._parent.addTopLevelItem(self)
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_IMAGE), image_thumbnail)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_FOCAL), focal_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_F_NUMBER), f_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_ISO), iso_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.A_LIGHTS), light_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.A_BORTLE), bortle_box)
        if os.path.isfile(small_brut_path):
            self._parent.setItemWidget(self, HEADERS.index(envs.G_PATH_BRUT), brut_thumbnail)

class AstroWorkspaceTree(WorkspaceTree):
    def __init__(self):
        super(AstroWorkspaceTree, self).__init__()

        self.setColumnCount(NB_SECTIONS)
        self.setHeaderLabels(HEADERS)

        # for header in HEADERS:
        #     self.header().setSectionResizeMode(HEADERS.index(header),
        #                             QtWidgets.QHeaderView.ResizeToContents)

        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)    
        self.header().setSectionHidden(1, True) # Path
        self.header().setSectionHidden(4, True) # Album
        self.setIconSize(QtCore.QSize(30,30))

    def add_item(self, file_row):
        item = AstroFileItem(self, file_row)
  
    def get_column_index(self, item, column):
        if column == HEADERS.index(envs.G_SUBJECT):
            return HEADERS.index(envs.G_SUBJECT)
        
    def update_item(self, server, item, column):
        db_column = None
        if column == HEADERS.index(envs.G_SUBJECT):
            db_column = api_envs.SUBJECT
        elif column == HEADERS.index(envs.G_DESC):
            db_column = api_envs.ALBUM
        elif column == HEADERS.index(envs.G_MAKE):
            db_column = api_envs.MAKE
        elif column == HEADERS.index(envs.G_MODEL):
            db_column = api_envs.MODEL
        elif column == HEADERS.index(envs.A_MOUNT):
            db_column = api_envs.MOUNT
        elif column == HEADERS.index(envs.G_FOCAL):
            db_column = api_envs.FOCAL
        elif column == HEADERS.index(envs.G_F_NUMBER):
            db_column = api_envs.F_NUMBER
        elif column == HEADERS.index(envs.G_ISO):
            db_column = api_envs.ISO
        elif column == HEADERS.index(envs.A_LIGHTS):
            db_column = api_envs.LIGHTS
        elif column == HEADERS.index(envs.G_EXPOSURE_TIME):
            db_column = api_envs.EXPOSURE_TIME
        elif column == HEADERS.index(envs.G_LOCATION):
            db_column = api_envs.LOCATION
        elif column == HEADERS.index(envs.A_BORTLE):
            db_column = api_envs.BORTLE
        elif column == HEADERS.index(envs.A_MOON_PHASE):
            db_column = api_envs.MOON_PHASE
        elif column == HEADERS.index(envs.G_SOFTWARE):
            db_column = api_envs.SOFTWARE
        elif column == HEADERS.index(envs.G_AUTHOR):
            db_column = api_envs.AUTHOR
        elif column == HEADERS.index(envs.G_COMMENT):
            db_column = api_envs.COMMENT
        elif column == HEADERS.index(envs.G_DATE):
            db_column = api_envs.DATE
        
        server._files.update(db_column, item.text(0), item.text(column))

        # item._update()

class AstroListWidget(QtWidgets.QListWidget):
    def __init__(self) -> None:
        super(AstroListWidget, self).__init__()

        self.setResizeMode(QtWidgets.QListView.Adjust)
        self.setViewMode(QtWidgets.QListWidget.IconMode)
        self.setFlow(QtWidgets.QListView.LeftToRight)
        self.setGridSize(QtCore.QSize(300,200))
        self.setSpacing(5)
        self.setWordWrap(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

    def add_item(self, data):
        # self.clear()
        thumbnail = ThumbnailButton(data[1])
        task_wdg_item = QtWidgets.QListWidgetItem()
        task_wdg_item.setSizeHint(thumbnail.sizeHint())

        self.addItem(task_wdg_item)
        self.setItemWidget(task_wdg_item, thumbnail)

        self.sortItems(QtCore.Qt.SortOrder.AscendingOrder)