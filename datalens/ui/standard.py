from PyQt5 import QtWidgets,QtCore, QtGui
from pathlib import Path
from datalens.ui.utils import WorkspaceTree, SpinWdg, ComboBoxWdg
from datalens.ui import envs
from datalens.api import envs as api_envs
from datalens.ui.image import ThumbnailButton, ImageInfosUI
from datalens.ui.utils import iso_color
import os

HEADERS = [envs.G_ID, envs.G_PATH, envs.G_IMAGE, 
           envs.G_SUBJECT, envs.G_DESC, envs.G_MAKE, envs.G_MODEL,
           envs.G_FOCAL, envs.G_F_NUMBER, envs.G_ISO,
           envs.G_EXPOSURE_TIME,
           envs.G_LOCATION, 
           envs.G_SOFTWARE, envs.G_AUTHOR, envs.G_COMMENT, envs.G_DATE,
           envs.G_PATH_BRUT]
NB_SECTIONS = len(HEADERS)

def idx(item):
        return HEADERS.index(item)

class StandardFileItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, db, id, contents = {}, *args, **kwargs):
        super(StandardFileItem, self).__init__(*args, **kwargs)
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
        img_path = Path(self._db._standard_files.get_path(self._id))
        self.setText(1, str(img_path))

        # subject
        self.setText(idx(envs.G_SUBJECT),
                     self._db._standard_files.get_subject(self._id))
        self.setFont(idx(envs.G_SUBJECT),
                     QtGui.QFont("Arial", 9, QtGui.QFont.Bold))
        
        # make
        self.setText(idx(envs.G_MAKE),
                     self._db._standard_files.get_make(self._id))
        contents = self._contents.get("maker", [])
        maker_cb = ComboBoxWdg(self,idx(envs.G_MAKE),
                               contents)
        
        # model
        self.setText(idx(envs.G_MODEL),
                     self._db._standard_files.get_model(self._id))
        contents = self._contents.get("model", [])
        model_cb = ComboBoxWdg(self,idx(envs.G_MODEL),
                               contents)
        
        # focal
        focal = self._db._standard_files.get_focal(self._id)
        self.setText(idx(envs.G_FOCAL), str(focal))
        focal_box = SpinWdg(self, idx(envs.G_FOCAL), int(focal))
        
        # f number
        f_number = self._db._standard_files.get_f_number(self._id)
        self.setText(idx(envs.G_F_NUMBER),
                     str(f_number))
        f_box = SpinWdg(self, idx(envs.G_F_NUMBER), float(f_number), mode="double")
        
        # iso
        iso = self._db._standard_files.get_iso(self._id)
        self.setText(idx(envs.G_ISO), str(iso))
        iso_box= SpinWdg(self, idx(envs.G_ISO), int(iso))
        self.setIcon(idx(envs.G_ISO), QtGui.QIcon(iso_color(iso)))

        # exposure
        exposure = self._db._standard_files.get_exposure_time(self._id)
        self.setText(idx(envs.G_EXPOSURE_TIME), str(exposure))
        exposure_box = SpinWdg(self, idx(envs.G_EXPOSURE_TIME),
                               float(exposure), mode="double")
       
        # location
        self.setText(idx(envs.G_LOCATION),
                     self._db._standard_files.get_location(self._id))
    
        # soft
        self.setText(idx(envs.G_SOFTWARE),
                     self._db._standard_files.get_software(self._id))
        contents = self._contents.get("software", [])
        soft_cb = ComboBoxWdg(self,idx(envs.G_SOFTWARE),
                               contents)
        
        # author
        self.setText(idx(envs.G_AUTHOR),
                     self._db._standard_files.get_author(self._id))
        contents = self._contents.get("author", [])
        author_cb = ComboBoxWdg(self,idx(envs.G_AUTHOR),
                               contents)
        # comment
        self.setText(idx(envs.G_COMMENT),
                     self._db._standard_files.get_comment(self._id))
        # date
        date = self._db._standard_files.get_date(self._id)
        self.setText(idx(envs.G_DATE), str(date))
        date_box = SpinWdg(self,idx(envs.G_DATE),date,mode="date")

        # get small image path
        small_image_path = img_path.parent / (img_path.stem + api_envs.IMAGE_SMALL_SUFFIX + img_path.suffix)
        self.image_thumbnail = ThumbnailButton(self._db, path=str(small_image_path),
                                               size=size)

        # get small brut path
        small_brut_path = img_path.parent / ("0" + api_envs.IMAGE_SMALL_SUFFIX + img_path.suffix)
        if os.path.isfile(small_brut_path):
            self.brut_thumbnail = ThumbnailButton(self._db, path=str(small_brut_path),
                                                  size=size)

        # ADD ITEM
        self._parent.addTopLevelItem(self)
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        idxs = [idx(envs.G_IMAGE),idx(envs.G_MAKE),idx(envs.G_MODEL),idx(envs.G_FOCAL),
            idx(envs.G_F_NUMBER),idx(envs.G_ISO),
            idx(envs.G_EXPOSURE_TIME),idx(envs.G_SOFTWARE),
            idx(envs.G_AUTHOR),idx(envs.G_DATE)]
        boxes = [self.image_thumbnail, maker_cb,model_cb, focal_box, f_box,
                 iso_box, exposure_box, soft_cb, author_cb, date_box]
        for i,b in zip(idxs,boxes):
            self._parent.setItemWidget(self, i, b)
    
        if os.path.isfile(small_brut_path):
            self._parent.setItemWidget(self, idx(envs.G_PATH_BRUT),
                                       self.brut_thumbnail)

class StandardWorkspaceTree(WorkspaceTree):
    def __init__(self, server):
        super(StandardWorkspaceTree, self).__init__(server)

        self.setColumnCount(NB_SECTIONS)
        self.setHeaderLabels(HEADERS)

        self.header().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)   
        self.header().setSectionHidden(1, True) # Path
        self.header().setSectionHidden(4, True) # Album

    def add_item(self, id):
        item = StandardFileItem(self, self._db, id, self._contents)
        self._items.append(item)
        
    def update_item(self, item, column):
        db_column = None
        if column == idx(envs.G_SUBJECT):
            db_column = api_envs.SUBJECT
        elif column == idx(envs.G_DESC):
            db_column = api_envs.ALBUM
        elif column == idx(envs.G_MAKE):
            db_column = api_envs.MAKE
        elif column == idx(envs.G_MODEL):
            db_column = api_envs.MODEL
        elif column == idx(envs.G_FOCAL):
            db_column = api_envs.FOCAL
        elif column == idx(envs.G_F_NUMBER):
            db_column = api_envs.F_NUMBER
        elif column == idx(envs.G_ISO):
            db_column = api_envs.ISO
        elif column == idx(envs.G_EXPOSURE_TIME):
            db_column = api_envs.EXPOSURE_TIME
        elif column == idx(envs.G_LOCATION):
            db_column = api_envs.LOCATION
        elif column == idx(envs.G_SOFTWARE):
            db_column = api_envs.SOFTWARE
        elif column == idx(envs.G_AUTHOR):
            db_column = api_envs.AUTHOR
        elif column == idx(envs.G_COMMENT):
            db_column = api_envs.COMMENT
        elif column == idx(envs.G_DATE):
            db_column = api_envs.DATE
        
        self._db._standard_files.update(db_column, item.text(0), item.text(column))
        self._contents = self.get_contents()

class StandardImageInfosUI(ImageInfosUI):
    def __init__(self, author=None, album_type=None):
        super().__init__()

    def create_layouts(self):
        font_bold = QtGui.QFont("Arial", 8, QtGui.QFont.Bold)
        for column_lbl in [self.subject_lbl, self.desc_lbl, self.date_lbl, self.location_lbl,
                           self.exposure_lbl, self.iso_lbl, self.aperture_lbl,
                           self.focal_lbl, self.author_lbl, self.model_lbl,
                           self.maker_lbl, self.process_lbl, self.comment_lbl]:
                column_lbl.setFont(font_bold)

        # Acquisition grid
        acquisition_gb = QtWidgets.QGroupBox("Acquisition Details")
        grid_layout = QtWidgets.QGridLayout(acquisition_gb)
        
        pos = 0
        for label, wdg in zip([self.date_lbl, self.location_lbl,
                               self.exposure_lbl, self.iso_lbl, self.aperture_lbl],
                              [self.date_le, self.location_le,
                               self.exposure_le, self.iso_le, self.aperture_le]):
            grid_layout.addWidget(label, pos, 0)
            grid_layout.addWidget(wdg, pos, 1)
            pos += 1
 
        self.v_layout.addWidget(acquisition_gb)
        self.v_layout.addWidget(self.location_btn)

        # Equipment grid
        equipment_gb = QtWidgets.QGroupBox("Equipment Details")
        grid_layout = QtWidgets.QGridLayout(equipment_gb)
        
        pos = 0
        for label, wdg in zip([self.maker_lbl,self.model_lbl, self.focal_lbl],
                              [self.maker_le, self.model_le, self.focal_le]):
            grid_layout.addWidget(label, pos, 0)
            grid_layout.addWidget(wdg, pos, 1)
            pos += 1
 
        self.v_layout.addWidget(equipment_gb)

        # more grid
        more_gb = QtWidgets.QGroupBox("More info")
        grid_layout = QtWidgets.QGridLayout(more_gb)
        
        pos = 0
        for label, wdg in zip([self.author_lbl, self.process_lbl, self.comment_lbl],
                              [self.author_le, self.process_le, self.comment_le]):
            grid_layout.addWidget(label, pos, 0)
            grid_layout.addWidget(wdg, pos, 1)
            pos += 1
 
        self.v_layout.addWidget(more_gb)

    def read(self):
        return {api_envs.ID : self._exif.get(api_envs.ID),
                api_envs.SUBJECT : self.subject_le.text(),
                api_envs.PATH : self._image_path,
                api_envs.ALBUM : self.album_le.text(),
                api_envs.MAKE : self.maker_le.text(),
                api_envs.MODEL : self.model_le.text(),
                api_envs.FOCAL : self.focal_le.value(),
                api_envs.F_NUMBER : self.aperture_le.value(),
                api_envs.ISO : self.iso_le.value(),
                api_envs.EXPOSURE_TIME : self.exposure_le.value(),
                api_envs.LOCATION : self.location_le.text(),
                api_envs.SOFTWARE : self.process_le.text(),
                api_envs.AUTHOR : self.author_le.text(),
                api_envs.COMMENT : self.comment_le.text(),
                api_envs.DATE : self.date_le.text(),
                api_envs.PATH_BRUT : self._brut_path}