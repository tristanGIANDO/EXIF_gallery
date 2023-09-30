from PyQt5 import QtWidgets,QtCore, QtGui
from pathlib import Path
from datalens.ui.utils import WorkspaceTree, SpinWdg, ComboBoxWdg
from datalens.ui import envs
from datalens.api import envs as api_envs
from datalens.ui.image import ThumbnailButton
from datalens.ui.utils import iso_color
import os

HEADERS = [envs.G_ID, envs.G_PATH, envs.G_IMAGE, 
           envs.G_SUBJECT, envs.G_DESC, envs.G_MAKE, envs.G_MODEL,
           envs.A_MOUNT, envs.G_FOCAL, envs.G_F_NUMBER, envs.G_ISO,
           envs.A_LIGHTS, envs.G_EXPOSURE_TIME, envs.A_TOTAL_TIME,
           envs.G_LOCATION, envs.A_BORTLE, envs.A_MOON_PHASE, 
           envs.G_SOFTWARE, envs.G_AUTHOR, envs.G_COMMENT, envs.G_DATE,
           envs.G_PATH_BRUT]
NB_SECTIONS = len(HEADERS)

def idx(item):
        return HEADERS.index(item)

class AstroFileItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, db, id, contents = {}, *args, **kwargs):
        super(AstroFileItem, self).__init__(*args, **kwargs)
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
        img_path = Path(self._db._astro_files.get_path(self._id))
        self.setText(1, str(img_path))

        # subject
        self.setText(idx(envs.G_SUBJECT),
                     self._db._astro_files.get_subject(self._id))
        self.setFont(idx(envs.G_SUBJECT),
                     QtGui.QFont("Arial", 9, QtGui.QFont.Bold))
        
        # make
        self.setText(idx(envs.G_MAKE),
                     self._db._astro_files.get_make(self._id))
        contents = self._contents.get("maker", [])
        maker_cb = ComboBoxWdg(self,idx(envs.G_MAKE),
                               contents)
        
        # model
        self.setText(idx(envs.G_MODEL),
                     self._db._astro_files.get_model(self._id))
        contents = self._contents.get("model", [])
        model_cb = ComboBoxWdg(self,idx(envs.G_MODEL),
                               contents)
        
        # mount
        self.setText(idx(envs.A_MOUNT),
                     self._db._astro_files.get_mount(self._id))
        
        # focal
        focal = self._db._astro_files.get_focal(self._id)
        self.setText(idx(envs.G_FOCAL), str(focal))
        focal_box = SpinWdg(self, idx(envs.G_FOCAL), int(focal))
        
        # f number
        f_number = self._db._astro_files.get_f_number(self._id)
        self.setText(idx(envs.G_F_NUMBER),
                     str(f_number))
        f_box = SpinWdg(self, idx(envs.G_F_NUMBER), float(f_number), mode="double")
        
        # iso
        iso = self._db._astro_files.get_iso(self._id)
        self.setText(idx(envs.G_ISO), str(iso))
        iso_box= SpinWdg(self, idx(envs.G_ISO), int(iso))
        self.setIcon(idx(envs.G_ISO), QtGui.QIcon(iso_color(iso)))
        
        # nb lights
        lights = self._db._astro_files.get_lights(self._id)
        self.setText(idx(envs.A_LIGHTS), str(lights))
        light_box= SpinWdg(self, idx(envs.A_LIGHTS), int(lights))

        # exposure
        exposure = self._db._astro_files.get_exposure_time(self._id)
        self.setText(idx(envs.G_EXPOSURE_TIME), str(exposure))
        exposure_box = SpinWdg(self, idx(envs.G_EXPOSURE_TIME),
                               float(exposure), mode="double")
        # total time
        self.setText(idx(envs.A_TOTAL_TIME),
                     self._db._astro_files.get_total_time(self._id)) # in UI ??
        # location
        self.setText(idx(envs.G_LOCATION),
                     self._db._astro_files.get_location(self._id))
        # bortle
        bortle = self._db._astro_files.get_bortle(self._id)
        self.setText(idx(envs.A_BORTLE), str(bortle))
        bortle_box = SpinWdg(self, idx(envs.A_BORTLE), int(bortle))
        
        # moon
        moon = self._db._astro_files.get_moon_phase(self._id)
        self.setText(idx(envs.A_MOON_PHASE), envs.MOON_PHASES.get(moon))
        self.setIcon(idx(envs.A_MOON_PHASE), envs.ICONS.get(moon))

        # soft
        self.setText(idx(envs.G_SOFTWARE),
                     self._db._astro_files.get_software(self._id))
        contents = self._contents.get("software", [])
        soft_cb = ComboBoxWdg(self,idx(envs.G_SOFTWARE),
                               contents)
        
        # author
        self.setText(idx(envs.G_AUTHOR),
                     self._db._astro_files.get_author(self._id))
        contents = self._contents.get("author", [])
        author_cb = ComboBoxWdg(self,idx(envs.G_AUTHOR),
                               contents)
        # comment
        self.setText(idx(envs.G_COMMENT),
                     self._db._astro_files.get_comment(self._id))
        # date
        date = self._db._astro_files.get_date(self._id)
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
            idx(envs.G_F_NUMBER),idx(envs.G_ISO),idx(envs.A_LIGHTS),
            idx(envs.A_BORTLE),idx(envs.G_EXPOSURE_TIME),idx(envs.G_SOFTWARE),
            idx(envs.G_AUTHOR),idx(envs.G_DATE)]
        boxes = [self.image_thumbnail, maker_cb,model_cb, focal_box, f_box,
                 iso_box, light_box, bortle_box, exposure_box, soft_cb, author_cb, date_box]
        for i,b in zip(idxs,boxes):
            self._parent.setItemWidget(self, i, b)
    
        if os.path.isfile(small_brut_path):
            self._parent.setItemWidget(self, idx(envs.G_PATH_BRUT),
                                       self.brut_thumbnail)

class AstroWorkspaceTree(WorkspaceTree):
    def __init__(self, server):
        super(AstroWorkspaceTree, self).__init__(server)

        self.setColumnCount(NB_SECTIONS)
        self.setHeaderLabels(HEADERS)

        self.header().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)   
        self.header().setSectionHidden(1, True) # Path
        self.header().setSectionHidden(4, True) # Album

    def add_item(self, id):
        item = AstroFileItem(self, self._db, id, self._contents)
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
        elif column == idx(envs.A_MOUNT):
            db_column = api_envs.MOUNT
        elif column == idx(envs.G_FOCAL):
            db_column = api_envs.FOCAL
        elif column == idx(envs.G_F_NUMBER):
            db_column = api_envs.F_NUMBER
        elif column == idx(envs.G_ISO):
            db_column = api_envs.ISO
        elif column == idx(envs.A_LIGHTS):
            db_column = api_envs.LIGHTS
        elif column == idx(envs.G_EXPOSURE_TIME):
            db_column = api_envs.EXPOSURE_TIME
        elif column == idx(envs.G_LOCATION):
            db_column = api_envs.LOCATION
        elif column == idx(envs.A_BORTLE):
            db_column = api_envs.BORTLE
        elif column == idx(envs.A_MOON_PHASE):
            db_column = api_envs.MOON_PHASE
        elif column == idx(envs.G_SOFTWARE):
            db_column = api_envs.SOFTWARE
        elif column == idx(envs.G_AUTHOR):
            db_column = api_envs.AUTHOR
        elif column == idx(envs.G_COMMENT):
            db_column = api_envs.COMMENT
        elif column == idx(envs.G_DATE):
            db_column = api_envs.DATE
        
        self._db._astro_files.update(db_column, item.text(0), item.text(column))
        self._contents = self.get_contents()