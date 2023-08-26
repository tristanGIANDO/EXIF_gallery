from PyQt5 import QtWidgets,QtCore, QtGui
from pathlib import Path
from datalens.ui_utils import WorkspaceTree, SpinWdg, ComboBoxWdg
from datalens import envs
from datalens.api import envs as api_envs
from datalens.ui_image import ThumbnailButton
import os

ICONS = envs.Icons()

HEADERS = [envs.G_ID, envs.G_PATH, envs.G_IMAGE, 
           envs.G_SUBJECT, envs.G_DESC, envs.G_MAKE, envs.G_MODEL,
           envs.A_MOUNT, envs.G_FOCAL, envs.G_F_NUMBER, envs.G_ISO,
           envs.A_LIGHTS, envs.G_EXPOSURE_TIME, envs.A_TOTAL_TIME,
           envs.G_LOCATION, envs.A_BORTLE, envs.A_MOON_PHASE, 
           envs.G_SOFTWARE, envs.G_AUTHOR, envs.G_COMMENT, envs.G_DATE,
           envs.G_PATH_BRUT]
NB_SECTIONS = len(HEADERS)

class AstroFileItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data, contents = {}, *args, **kwargs):
        super(AstroFileItem, self).__init__(*args, **kwargs)
        if not data:
            return
        self._parent = parent
        self._data = data
        self._contents = contents
        self._update()

    def set_column(self,idx, inc=1, font=False):
        self.setText(idx, str(self._data[idx-inc]))
        if font:
            self.setFont(idx, QtGui.QFont("Arial", 9, QtGui.QFont.Bold))

    def _update(self):
        #id
        self.setText(0, self._data[0]) 
        # path
        img_path = Path(self._data[1])
        self.setText(1, str(img_path))

        for i in range(2,NB_SECTIONS):
            self.setTextAlignment(i, QtCore.Qt.AlignCenter)
            if i % 2 == 0:
                self.setBackground(i, QtGui.QColor(240,240,240))
        
        # subject
        self.set_column(HEADERS.index(envs.G_SUBJECT), font=True)
        # make
        self.set_column(HEADERS.index(envs.G_MAKE))
        contents = self._contents.get("maker", [])
        maker_cb = ComboBoxWdg(self,HEADERS.index(envs.G_MAKE),
                               contents)
        # model
        self.set_column(HEADERS.index(envs.G_MODEL))
        contents = self._contents.get("model", [])
        model_cb = ComboBoxWdg(self,HEADERS.index(envs.G_MODEL),
                               contents)
        # mount
        self.set_column(HEADERS.index(envs.A_MOUNT))
        # focal
        self.set_column(HEADERS.index(envs.G_FOCAL))
        focal_box = SpinWdg(self, HEADERS.index(envs.G_FOCAL),
                            int(self._data[HEADERS.index(envs.G_FOCAL)-1]))
        # f number
        self.set_column(HEADERS.index(envs.G_F_NUMBER))
        f_box = SpinWdg(self, HEADERS.index(envs.G_F_NUMBER), 
                        float(self._data[HEADERS.index(envs.G_F_NUMBER)-1]), 
                        mode="double")
        # iso
        idx = HEADERS.index(envs.G_ISO)
        self.set_column(idx)
        iso_box= SpinWdg(self, idx,
                         int(self._data[idx-1]))

        r = int(self._data[HEADERS.index(envs.G_ISO)-1]/100*3.5)
        if r > 255:
            r = 255
        iso_color = QtGui.QColor(r, 100, 30)
        iso_icon = QtGui.QPixmap(20,20)
        iso_icon.fill(iso_color)
        self.setIcon(HEADERS.index(envs.G_ISO), QtGui.QIcon(iso_icon))
        # nb lights
        idx = HEADERS.index(envs.A_LIGHTS)
        self.set_column(idx)
        light_box= SpinWdg(self, idx,
                         int(self._data[idx-1]))
        # exposure
        # self.setIcon(HEADERS.index(envs.G_EXPOSURE_TIME), ICONS.get("x"))
        exposure_box = SpinWdg(self, HEADERS.index(envs.G_EXPOSURE_TIME), 
                               float(self._data[HEADERS.index(envs.G_EXPOSURE_TIME)-1]), 
                               mode="double")
        # total time
        # self.setIcon(HEADERS.index(envs.A_TOTAL_TIME), ICONS.get("="))
        self.set_column(HEADERS.index(envs.A_TOTAL_TIME), font=True)
        # location
        self.set_column(HEADERS.index(envs.G_LOCATION))
        # bortle
        self.set_column(HEADERS.index(envs.A_BORTLE))
        bortle_box = SpinWdg(self, HEADERS.index(envs.A_BORTLE), 
                             int(self._data[HEADERS.index(envs.A_BORTLE)-1]))
        # moon
        i = HEADERS.index(envs.A_MOON_PHASE)
        self.setText(i, envs.MOON_PHASES.get(self._data[i-1]))
        self.setIcon(HEADERS.index(envs.A_MOON_PHASE),
                     ICONS.get(self._data[15]))
        # soft
        self.set_column(HEADERS.index(envs.G_SOFTWARE))
        contents = self._contents.get("software", [])
        soft_cb = ComboBoxWdg(self,HEADERS.index(envs.G_SOFTWARE),
                               contents)
        # author
        self.set_column(HEADERS.index(envs.G_AUTHOR))
        contents = self._contents.get("author", [])
        author_cb = ComboBoxWdg(self,HEADERS.index(envs.G_AUTHOR),
                               contents)
        # comment
        self.set_column(HEADERS.index(envs.G_COMMENT))
        # date
        self.set_column(HEADERS.index(envs.G_DATE))
        date_box = SpinWdg(self, HEADERS.index(envs.G_DATE), 
                           self._data[HEADERS.index(envs.G_DATE)-1], 
                           mode="date")

        # get small image path
        small_image_path = img_path.parent / (img_path.stem + api_envs.IMAGE_SMALL_SUFFIX + img_path.suffix)
        image_thumbnail = ThumbnailButton(path=str(small_image_path))

        # get small brut path
        small_brut_path = img_path.parent / (img_path.stem + api_envs.BRUT_SMALL_SUFFIX + img_path.suffix)
        if os.path.isfile(small_brut_path):
            brut_thumbnail = ThumbnailButton(path=str(small_brut_path))

        # ADD ITEM
        self._parent.addTopLevelItem(self)
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_IMAGE), image_thumbnail)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_MAKE), maker_cb)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_MODEL), model_cb)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_FOCAL), focal_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_F_NUMBER), f_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_ISO), iso_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.A_LIGHTS), light_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.A_BORTLE), bortle_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_EXPOSURE_TIME), exposure_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_SOFTWARE), soft_cb)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_AUTHOR), author_cb)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_DATE), date_box)
        if os.path.isfile(small_brut_path):
            self._parent.setItemWidget(self, HEADERS.index(envs.G_PATH_BRUT), brut_thumbnail)

class AstroWorkspaceTree(WorkspaceTree):
    def __init__(self, server):
        super(AstroWorkspaceTree, self).__init__()

        self._server = server
        self._contents = self.get_contents()
        self.setColumnCount(NB_SECTIONS)
        self.setHeaderLabels(HEADERS)

        self.header().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)   
        self.header().setSectionHidden(1, True) # Path
        self.header().setSectionHidden(4, True) # Album
        self.setIconSize(QtCore.QSize(30,30))

    def add_item(self, file_row):
        item = AstroFileItem(self, file_row, self._contents)
  
    def get_column_index(self, item, column):
        if column == HEADERS.index(envs.G_SUBJECT):
            return HEADERS.index(envs.G_SUBJECT)
        
    def update_item(self, item, column):
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
        
        self._server._files.update(db_column, item.text(0), item.text(column))
        self._contents = self.get_contents()

    def get_contents(self):
        def check(p_list, col, item):
            x = self._server._files.get(col, item)
            if x and x not in p_list:
                p_list.append(x[0][0])
            return p_list
        
        models = []
        makers = []
        authors = []
        softs = []
        for file in self._server._files.select_rows():
            makers = check(makers, "make", file[0])
            models = check(models, "model", file[0])
            authors = check(authors, "author", file[0])
            softs = check(softs, "software", file[0])
            
        return {
            "maker" : makers,
            "model" : models,
            "author" : authors,
            "software" : softs
            }

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