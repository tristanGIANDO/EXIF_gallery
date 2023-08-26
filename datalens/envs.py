from PyQt5 import QtGui
import os

class Icons():
    def __init__(self):
        self._root = os.path.join(os.path.dirname(__file__), "icons")
        self._cache = {}

    def get(self, key):
        if key in self._cache:
            return self._cache[key]
        
        path = os.path.join(self._root, ICONS.get(key))
        icon = QtGui.QIcon(path)
        self._cache[path] = icon
        return icon

ICONS = {
    "logo" : "logo.png",
    "add_file" : "add_image.png",
    "remove_file" : "remove_image.png",
    "add_album" : "add_album.png",
    "add_version" : "add_version.png",
    "remove_album" : "remove_album.png",
    "reload" : "reload.png",
    "full" : "full_screen.png",
    "previous" : "arrow_left.png",
    "next" : "arrow_right.png",
    "list" : "list.png",
    "card" : "card.png",
    "viewer" : "viewer.png",
    "website" : "website.png",
    "user" : "user.png",
    "graph" : "graph.png",
    0 : "0.png",
    1 : "1.png",
    2 : "2.png",
    3 : "3.png",
    4 : "4.png",
    5 : "5.png",
    6 : "6.png",
    7 : "7.png"
}

# global infos
G_ID = "ID"
G_PATH = "Path"
G_IMAGE = "Image"
G_ALBUM = "Album"
G_SUBJECT = "Subject"
G_DESC = "Description"
G_MAKE = "Maker"
G_MODEL = "Camera"
G_FOCAL = "Focal Length (mm)"
G_F_NUMBER = "Aperture"
G_ISO = "ISO"
G_EXPOSURE_TIME = "Exposure Time (seconds)"
G_LOCATION = "Location"
G_SOFTWARE = "Processed with"
G_AUTHOR = "Author"
G_COMMENT = "Comment"
G_DATE = "Date"
G_PATH_BRUT = "Brut"

# astro infos
A_MOUNT = "Mount"
A_LIGHTS = "NB Lights"
A_BORTLE = "Sky Darkness"
A_MOON_PHASE = "Moon Phase"
A_TOTAL_TIME = "Total Time"

MOON_PHASES = {
      0: "New Moon", 
      1: "Waxing Crescent", 
      2: "First Quarter", 
      3: "Waxing Gibbous", 
      4: "Full Moon", 
      5: "Waning Gibbous", 
      6: "Last Quarter", 
      7: "Waning Crescent"
   }