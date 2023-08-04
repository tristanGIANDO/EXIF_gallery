from PyQt5 import QtWidgets,QtCore, QtGui
from ui_utils import WorkspaceTree, ImageViewWidget
import envs

HEADERS = [envs.G_ID, envs.G_PATH, envs.G_IMAGE, envs.G_SUBJECT, envs.G_DESC,
           envs.G_CAMERA, envs.G_FOCAL, envs.A_MOUNT, envs.G_APERTURE,
           envs.G_ISO, envs.A_LIGHTS, envs.G_EXPOSURE_TIME, 
           envs.A_TIME, envs.G_LOCATION, envs.A_BORTLE, envs.A_MOON, 
           envs.G_PROCESS, envs.G_AUTHOR, envs.G_COMMENT, envs.G_DATE]
NB_SECTIONS = len(HEADERS)

class AstroFileItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, data, *args, **kwargs):

        super(AstroFileItem, self).__init__(*args, **kwargs)

        if data and len(data) == 19:
            self.setText(HEADERS.index(envs.G_ID), str(data[0]))
            self.setText(HEADERS.index(envs.G_PATH), data[1])
            self.setText(HEADERS.index(envs.G_SUBJECT), data[2])
            self.setText(HEADERS.index(envs.G_DESC), data[3])
            self.setText(HEADERS.index(envs.G_CAMERA), data[4])
            self.setText(HEADERS.index(envs.A_MOUNT), data[5])
            self.setText(HEADERS.index(envs.G_FOCAL), str(data[6]))
            self.setText(HEADERS.index(envs.G_APERTURE), "f/" + str(data[7]))
            self.setText(HEADERS.index(envs.G_ISO), str(data[8]))
            self.setText(HEADERS.index(envs.A_LIGHTS), str(data[9]))
            self.setText(HEADERS.index(envs.G_EXPOSURE_TIME), str(data[10]))
            self.setText(HEADERS.index(envs.A_TIME), str(data[11]))
            self.setText(HEADERS.index(envs.G_LOCATION), data[12])
            self.setText(HEADERS.index(envs.A_BORTLE), str(data[13]))
            self.setText(HEADERS.index(envs.A_MOON), envs.MOON_PHASES.get(data[14]))
            self.setText(HEADERS.index(envs.G_PROCESS), data[15])
            self.setText(HEADERS.index(envs.G_AUTHOR), data[16])
            self.setText(HEADERS.index(envs.G_COMMENT), data[17])
            self.setText(HEADERS.index(envs.G_DATE), data[18])

            self.setIcon(HEADERS.index(envs.A_MOON), QtGui.QIcon(envs.ICONS[data[14]]))
        
        thumbnail = ImageViewWidget(data[1])
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
            db_column = "subject"
        elif column == HEADERS.index(envs.G_DESC):
            db_column = "description"
        elif column == HEADERS.index(envs.G_CAMERA):
            db_column = "camera"
        elif column == HEADERS.index(envs.A_MOUNT):
            db_column = "mount"
        elif column == HEADERS.index(envs.G_FOCAL):
            db_column = "focal"
        elif column == HEADERS.index(envs.G_APERTURE):
            db_column = "aperture"
        elif column == HEADERS.index(envs.G_ISO):
            db_column = "iso"
        elif column == HEADERS.index(envs.A_LIGHTS):
            db_column = "lights"
        elif column == HEADERS.index(envs.G_EXPOSURE_TIME):
            db_column = "exposure"
        elif column == HEADERS.index(envs.G_LOCATION):
            db_column = "place"
        elif column == HEADERS.index(envs.A_BORTLE):
            db_column = "bortle"
        elif column == HEADERS.index(envs.A_MOON):
            db_column = "moon"
        elif column == HEADERS.index(envs.G_PROCESS):
            db_column = "processed"
        elif column == HEADERS.index(envs.G_AUTHOR):
            db_column = "author"
        elif column == HEADERS.index(envs.G_COMMENT):
            db_column = "comment"
        elif column == HEADERS.index(envs.G_DATE):
            db_column = "date"
        
        server.update(db_column, item.text(0), item.text(column))