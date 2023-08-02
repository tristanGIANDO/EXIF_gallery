from PyQt5 import QtWidgets,QtCore
from image_ui import ImageViewWidget
from ws_ui import WorkspaceTree

I_ID = "ID"
I_PATH = "Path"
I_IMAGE = "Image"
I_SUBJECT = "Subject"
I_DESC = "Description"
I_CAMERA = "Camera"
I_FOCAL = "Focal Length (mm)"
I_MOUNT = "Mount"
I_APERTURE = "Aperture"
I_ISO = "ISO"
I_LIGHTS = "NB Lights"
I_EXPOSURE_TIME = "Exposure Time (s)"
I_TIME = "Total Time"
I_PLACE = "Place"
I_BORTLE = "Sky Darkness"
I_MOON = "Moon Illumination"
I_PROCESS = "Processed with"
I_AUTHOR = "Author"
I_COMMENT = "Comment"
I_DATE = "Date"

HEADERS = [I_ID, I_PATH, I_IMAGE, I_SUBJECT, I_DESC,
           I_CAMERA, I_FOCAL, I_MOUNT, I_APERTURE,
           I_ISO, I_LIGHTS, I_EXPOSURE_TIME, 
           I_TIME, I_PLACE, I_BORTLE, I_MOON, 
           I_PROCESS, I_AUTHOR, I_COMMENT, I_DATE]
NB_SECTIONS = len(HEADERS)

class AstroFileItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, data, *args, **kwargs):

        super(AstroFileItem, self).__init__(*args, **kwargs)

        if data and len(data) == 19:
            self.setText(HEADERS.index(I_ID), str(data[0]))
            self.setText(HEADERS.index(I_PATH), data[1])
            self.setText(HEADERS.index(I_SUBJECT), data[2])
            self.setText(HEADERS.index(I_DESC), data[3])
            self.setText(HEADERS.index(I_CAMERA), data[4])
            self.setText(HEADERS.index(I_MOUNT), data[5])
            self.setText(HEADERS.index(I_FOCAL), str(data[6]))
            self.setText(HEADERS.index(I_APERTURE), "f/" + str(data[7]))
            self.setText(HEADERS.index(I_ISO), str(data[8]))
            self.setText(HEADERS.index(I_LIGHTS), str(data[9]))
            self.setText(HEADERS.index(I_EXPOSURE_TIME), str(data[10]))
            self.setText(HEADERS.index(I_TIME), str(data[11]))
            self.setText(HEADERS.index(I_PLACE), data[12])
            self.setText(HEADERS.index(I_BORTLE), str(data[13]))
            self.setText(HEADERS.index(I_MOON), str(data[14]) + "%")
            self.setText(HEADERS.index(I_PROCESS), data[15])
            self.setText(HEADERS.index(I_AUTHOR), data[16])
            self.setText(HEADERS.index(I_COMMENT), data[17])
            self.setText(HEADERS.index(I_DATE), data[18])

class AstroWorkspaceTree(WorkspaceTree):
    def __init__(self):
        super(AstroWorkspaceTree, self).__init__()

        self.setColumnCount(NB_SECTIONS)
        self.setHeaderLabels(HEADERS)

        for header in HEADERS:
            self.header().setSectionResizeMode(HEADERS.index(header),
                                    QtWidgets.QHeaderView.ResizeToContents)
            
        self.header().setSectionHidden(1, True) # Path

    def add_tree_item(self, file_row):
        item = AstroFileItem(file_row)
        thumbnail = ImageViewWidget(file_row[1])
        # focal_box = QtWidgets.QSpinBox()

        self.addTopLevelItem(item)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.setItemWidget(item, HEADERS.index(I_IMAGE), thumbnail)
        # self.setItemWidget(item, HEADERS.index(I_FOCAL), focal_box)

    def get_column_index(self, item, column):
        if column == HEADERS.index(I_SUBJECT):
            return HEADERS.index(I_SUBJECT)
        
    def update_item(self, server, item, column):
        db_column = None
        if column == HEADERS.index(I_SUBJECT):
            db_column = "subject"
        elif column == HEADERS.index(I_DESC):
            db_column = "description"
        elif column == HEADERS.index(I_CAMERA):
            db_column = "camera"
        elif column == HEADERS.index(I_MOUNT):
            db_column = "mount"
        elif column == HEADERS.index(I_FOCAL):
            db_column = "focal"
        elif column == HEADERS.index(I_APERTURE):
            db_column = "aperture"
        elif column == HEADERS.index(I_ISO):
            db_column = "iso"
        elif column == HEADERS.index(I_LIGHTS):
            db_column = "lights"
        elif column == HEADERS.index(I_EXPOSURE_TIME):
            db_column = "exposure"
        elif column == HEADERS.index(I_PLACE):
            db_column = "place"
        elif column == HEADERS.index(I_BORTLE):
            db_column = "bortle"
        elif column == HEADERS.index(I_MOON):
            db_column = "moon"
        elif column == HEADERS.index(I_PROCESS):
            db_column = "processed"
        elif column == HEADERS.index(I_AUTHOR):
            db_column = "author"
        elif column == HEADERS.index(I_COMMENT):
            db_column = "comment"
        elif column == HEADERS.index(I_DATE):
            db_column = "date"
        
        server.update(db_column, item.text(0), item.text(column))