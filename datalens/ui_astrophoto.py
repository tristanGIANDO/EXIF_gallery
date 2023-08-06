from PyQt5 import QtWidgets,QtCore, QtGui
from pathlib import Path
from ui_utils import WorkspaceTree, ImageViewWidget
import envs
from api import envs as api_envs

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
        
        path = Path(data[1])
        self.setText(0, data[0]) #id
        self.setText(1, str(path)) #path
        for i in range(2,NB_SECTIONS):
            if i == HEADERS.index(envs.A_MOON_PHASE):
                self.setText(i, envs.MOON_PHASES.get(data[i-1]))
            else:
                try:
                    self.setText(i+1, str(data[i]))
                except:
                    pass
            if i % 2 == 0:
                self.setBackground(i, QtGui.QColor(240,240,240))
        
        
        self.setIcon(HEADERS.index(envs.A_MOON_PHASE), QtGui.QIcon(envs.ICONS[data[15]]))
    
        # get small image path
        small_path = path.parent / (path.stem + api_envs.IMAGE_SMALL_SUFFIX + path.suffix)
        thumbnail = ImageViewWidget(str(small_path))
        # focal_box = QtWidgets.QSpinBox()

        parent.addTopLevelItem(self)
        self.setFlags(self.flags() | QtCore.Qt.ItemIsEditable)
        parent.setItemWidget(self, HEADERS.index(envs.G_IMAGE), thumbnail)

class AstroWorkspaceTree(WorkspaceTree):
    def __init__(self):
        super(AstroWorkspaceTree, self).__init__()

        self.setColumnCount(NB_SECTIONS)
        self.setHeaderLabels(HEADERS)

        for header in HEADERS:
            self.header().setSectionResizeMode(HEADERS.index(header),
                                    QtWidgets.QHeaderView.ResizeToContents)
            
        self.header().setSectionHidden(1, True) # Path
        self.setIconSize(QtCore.QSize(30,30))

    def add_tree_item(self, file_row):
        item = AstroFileItem(self, file_row)
  
    def get_column_index(self, item, column):
        if column == HEADERS.index(envs.G_SUBJECT):
            return HEADERS.index(envs.G_SUBJECT)
        
    def update_item(self, server, item, column):
        db_column = None
        if column == HEADERS.index(envs.G_SUBJECT):
            db_column = api_envs.SUBJECT
        elif column == HEADERS.index(envs.G_DESC):
            db_column = api_envs.DESC
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