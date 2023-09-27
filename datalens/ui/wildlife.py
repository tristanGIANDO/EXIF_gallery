from PyQt5 import QtWidgets,QtCore, QtGui
from pathlib import Path
from datalens.ui.utils import WorkspaceTree, SpinWdg, ComboBoxWdg
from datalens.ui import envs
from datalens.api import envs as api_envs
from datalens.ui.image import ThumbnailButton
import os

HEADERS = [envs.G_ID, envs.G_PATH, envs.G_IMAGE, 
           envs.G_SUBJECT, envs.G_DESC, envs.G_MAKE, envs.G_MODEL,
           envs.A_MOUNT, envs.G_FOCAL, envs.G_F_NUMBER, envs.G_ISO,
           envs.G_EXPOSURE_TIME,
           envs.G_LOCATION,
           envs.G_SOFTWARE, envs.G_AUTHOR, envs.G_COMMENT, envs.G_DATE,
           envs.G_PATH_BRUT]
NB_SECTIONS = len(HEADERS)

class WildLifeFilteItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, db, id, contents = {}, *args, **kwargs):
        super(WildLifeFilteItem, self).__init__(*args, **kwargs)
        self._parent = parent
        self._db = db
        self._id = id
        self._contents = contents

        for i in range(2,NB_SECTIONS):
            self.setTextAlignment(i, QtCore.Qt.AlignCenter)
            if i % 2 == 0:
                self.setBackground(i, QtGui.QColor(240,240,240))

        self.setSizeHint(2,QtCore.QSize(20,20))

        self._update()

    def _update(self, size = None):
        #id
        self.setText(0, self._id)

        # path
        img_path = Path(self._db._files.get_path(self._id))
        self.setText(1, str(img_path))

        # subject
        self.setText(HEADERS.index(envs.G_SUBJECT),
                     self._db._files.get_subject(self._id))
        self.setFont(HEADERS.index(envs.G_SUBJECT),
                     QtGui.QFont("Arial", 9, QtGui.QFont.Bold))
        
        # make
        self.setText(HEADERS.index(envs.G_MAKE),
                     self._db._files.get_make(self._id))
        contents = self._contents.get("maker", [])
        maker_cb = ComboBoxWdg(self,HEADERS.index(envs.G_MAKE),
                               contents)
        
        # model
        self.setText(HEADERS.index(envs.G_MODEL),
                     self._db._files.get_model(self._id))
        contents = self._contents.get("model", [])
        model_cb = ComboBoxWdg(self,HEADERS.index(envs.G_MODEL),
                               contents)
        
        # mount
        self.setText(HEADERS.index(envs.A_MOUNT),
                     self._db._files.get_mount(self._id))
        
        # focal
        focal = self._db._files.get_focal(self._id)
        self.setText(HEADERS.index(envs.G_FOCAL), str(focal))
        focal_box = SpinWdg(self, HEADERS.index(envs.G_FOCAL), int(focal))
        
        # f number
        f_number = self._db._files.get_f_number(self._id)
        self.setText(HEADERS.index(envs.G_F_NUMBER),
                     str(f_number))
        f_box = SpinWdg(self, HEADERS.index(envs.G_F_NUMBER), float(f_number), mode="double")
        
        # iso
        iso = self._db._files.get_iso(self._id)
        self.setText(HEADERS.index(envs.G_ISO), str(iso))
        iso_box= SpinWdg(self, HEADERS.index(envs.G_ISO), int(iso))
        r = int(iso/100*3.5)
        if r > 255:
            r = 255
        iso_color = QtGui.QColor(r, 100, 30)
        iso_icon = QtGui.QPixmap(20,20)
        iso_icon.fill(iso_color)
        self.setIcon(HEADERS.index(envs.G_ISO), QtGui.QIcon(iso_icon))

        # exposure
        exposure = self._db._files.get_exposure_time(self._id)
        self.setText(HEADERS.index(envs.G_EXPOSURE_TIME), str(exposure))
        exposure_box = SpinWdg(self, HEADERS.index(envs.G_EXPOSURE_TIME),
                               float(exposure), mode="double")

        # location
        self.setText(HEADERS.index(envs.G_LOCATION),
                     self._db._files.get_location(self._id))

        # soft
        self.setText(HEADERS.index(envs.G_SOFTWARE),
                     self._db._files.get_software(self._id))
        contents = self._contents.get("software", [])
        soft_cb = ComboBoxWdg(self,HEADERS.index(envs.G_SOFTWARE),
                               contents)
        
        # author
        self.setText(HEADERS.index(envs.G_AUTHOR),
                     self._db._files.get_author(self._id))
        contents = self._contents.get("author", [])
        author_cb = ComboBoxWdg(self,HEADERS.index(envs.G_AUTHOR),
                               contents)
        # comment
        self.setText(HEADERS.index(envs.G_COMMENT),
                     self._db._files.get_comment(self._id))
        # date
        date = self._db._files.get_date(self._id)
        self.setText(HEADERS.index(envs.G_DATE), str(date))
        date_box = SpinWdg(self,HEADERS.index(envs.G_DATE),date,mode="date")

        # get small image path
        small_image_path = img_path.parent / (img_path.stem + api_envs.IMAGE_SMALL_SUFFIX + img_path.suffix)
        self.image_thumbnail = ThumbnailButton(path=str(small_image_path),
                                               size=size)

        # get small brut path
        small_brut_path = img_path.parent / ("0" + api_envs.IMAGE_SMALL_SUFFIX + img_path.suffix)
        if os.path.isfile(small_brut_path):
            self.brut_thumbnail = ThumbnailButton(path=str(small_brut_path),
                                                  size=size)

        # ADD ITEM
        self._parent.addTopLevelItem(self)
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_IMAGE), self.image_thumbnail)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_MAKE), maker_cb)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_MODEL), model_cb)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_FOCAL), focal_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_F_NUMBER), f_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_ISO), iso_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_EXPOSURE_TIME), exposure_box)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_SOFTWARE), soft_cb)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_AUTHOR), author_cb)
        self._parent.setItemWidget(self, HEADERS.index(envs.G_DATE), date_box)
        if os.path.isfile(small_brut_path):
            self._parent.setItemWidget(self, HEADERS.index(envs.G_PATH_BRUT),
                                       self.brut_thumbnail)

class WildLifeTree(WorkspaceTree):
    def __init__(self, server):
        super(WildLifeTree, self).__init__()

        self._db = server
        self._contents = self.get_contents()
        self._items = []

        self.setColumnCount(NB_SECTIONS)
        self.setHeaderLabels(HEADERS)

        self.header().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)   
        self.header().setSectionHidden(1, True) # Path
        self.header().setSectionHidden(4, True) # Album
        self.setIconSize(QtCore.QSize(30,30))

    def add_item(self, id):
        item = WildLifeFilteItem(self, self._db, id, self._contents)
        self._items.append(item)
  
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
        elif column == HEADERS.index(envs.G_EXPOSURE_TIME):
            db_column = api_envs.EXPOSURE_TIME
        elif column == HEADERS.index(envs.G_LOCATION):
            db_column = api_envs.LOCATION
        elif column == HEADERS.index(envs.G_SOFTWARE):
            db_column = api_envs.SOFTWARE
        elif column == HEADERS.index(envs.G_AUTHOR):
            db_column = api_envs.AUTHOR
        elif column == HEADERS.index(envs.G_COMMENT):
            db_column = api_envs.COMMENT
        elif column == HEADERS.index(envs.G_DATE):
            db_column = api_envs.DATE
        
        self._db._files.update(db_column, item.text(0), item.text(column))
        self._contents = self.get_contents()

    def get_contents(self):
        def check(p_list, col, item):
            x = self._db._files.get(col, item)
            if x and x not in p_list:
                p_list.append(x[0][0])
            return p_list
        
        models = []
        makers = []
        authors = []
        softs = []
        for file in self._db._files.select_rows():
            makers = check(makers, "make", file[0])
            models = check(models, "model", file[0])
            authors = check(authors, "author", file[0])
            softs = check(softs, "software", file[0])
            
        return {
            "maker" : list(set(makers)),
            "model" : list(set(models)),
            "author" : list(set(authors)),
            "software" : list(set(softs))
            }

    def get_items(self):
        return self._items
        
class WildLifeListWidget(QtWidgets.QListWidget):
    def __init__(self) -> None:
        super(WildLifeListWidget, self).__init__()

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