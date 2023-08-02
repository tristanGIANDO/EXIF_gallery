import os

icons_root = os.path.join(os.path.dirname(__file__), "icons")

ICONS = {
    "add_file" : f"{icons_root}/add_image.png",
    "remove_file" : f"{icons_root}/remove_image.png",
    "reload" : f"{icons_root}/reload.png"
}

G_ID = "ID"
G_PATH = "Path"
G_IMAGE = "Image"
G_SUBJECT = "Subject"
G_DESC = "Description"
G_CAMERA = "Camera"
G_FOCAL = "Focal Length (mm)"
A_MOUNT = "Mount"
G_APERTURE = "Aperture"
G_ISO = "ISO"
A_LIGHTS = "NB Lights"
G_EXPOSURE_TIME = "Exposure Time (seconds)"
A_TIME = "Total Time"
G_LOCATION = "Location"
A_BORTLE = "Sky Darkness"
A_MOON = "Moon Phase"
G_PROCESS = "Processed with"
G_AUTHOR = "Author"
G_COMMENT = "Comment"
G_DATE = "Date"