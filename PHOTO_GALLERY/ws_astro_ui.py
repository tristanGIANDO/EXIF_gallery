from PyQt5 import QtWidgets,QtCore
from image_ui import ImageViewWidget
from ws_ui import WorkspaceTree

I_ID = "ID"
I_PATH = "Path"
I_IMAGE = "Image"
I_SUBJECT = "Subject"
I_DESC = "Description"
I_CAMERA = "Camera"
I_FOCAL = "Focal Length"
I_MOUNT = "Mount"
I_APERTURE = "Aperture"
I_ISO = "ISO"
I_LIGHTS = "NB Lights"
I_EXPOSURE_TIME = "Exposure Time"
I_TIME = "Total Time"
I_PLACE = "Sky Darkness"
I_MOON = "Moon Illumination"
I_PROCESS = "Processed with"
I_AUTHOR = "Author"
I_COMMENT = "Comment"

HEADERS = [I_ID, I_PATH, I_IMAGE, I_SUBJECT, I_DESC,
           I_CAMERA, I_FOCAL, I_MOUNT, I_APERTURE,
           I_ISO, I_LIGHTS, I_EXPOSURE_TIME, 
           I_TIME, I_PLACE, I_MOON, 
           I_PROCESS, I_AUTHOR, I_COMMENT]
NB_SECTIONS = len(HEADERS)

class AstroFileItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, data, *args, **kwargs):

        super(AstroFileItem, self).__init__(*args, **kwargs)

        if data:
            self.setText(HEADERS.index(I_ID), str(data[0]))
            self.setText(HEADERS.index(I_SUBJECT), data[1])
            self.setText(HEADERS.index(I_PATH), data[2])
            self.setText(HEADERS.index(I_AUTHOR), data[3])
            self.setText(HEADERS.index(I_COMMENT), data[4])

class AstroWorkspaceTree(WorkspaceTree):
    def __init__(self):
        super(AstroWorkspaceTree, self).__init__()

        self.setColumnCount(NB_SECTIONS)
        self.setHeaderLabels(HEADERS)

        for header in HEADERS:
            if HEADERS.index(header) == HEADERS.index(I_SUBJECT):
                continue
            self.header().setSectionResizeMode(HEADERS.index(header),
                                    QtWidgets.QHeaderView.ResizeToContents)

    def add_tree_item(self, file_row):
        item = AstroFileItem(file_row)
        thumbnail = ImageViewWidget(file_row[2])
        focal_box = QtWidgets.QSpinBox()

        self.addTopLevelItem(item)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.setItemWidget(item, HEADERS.index(I_IMAGE), thumbnail)
        self.setItemWidget(item, HEADERS.index(I_FOCAL), focal_box)

    def get_column_index(self, item, column):
        if column == HEADERS.index(I_SUBJECT):
            return HEADERS.index(I_SUBJECT)
        
    def update_item(self, server, item, column):
        db_column = None
        if column == HEADERS.index(I_SUBJECT):
            db_column = "name"
        elif column == HEADERS.index(I_AUTHOR):
            db_column = "author"
        
        server.update(db_column, item.text(0), item.text(column))