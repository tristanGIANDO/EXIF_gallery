import os

DB_NAME = "db01"
FILE_TABLE_NAME = "files"

ROOT = os.path.join(os.path.expanduser("~"), ".database")

ID = "id"
PATH = "path"
SUBJECT = "subject"
DESC = "description"
CAMERA = "camera"
MOUNT = "mount"
FOCAL = "focal"
APERTURE = "aperture"
ISO = "iso"
LIGHTS = "lights"
EXPOSURE_TIME = "exposure"
TIME = "time"
PLACE = "place"
BORTLE = "bortle"
MOON = "moon"
PROCESS = "processed"
AUTHOR = "author"
COMMENT = "comment"
DATE = "date"


# Exif file
F_KEY = "_key"
F_NAME = "_name"
F_PATH = "_path"
F_IMAGE = "_image"
F_DESCRIPTION = 270
F_MAKE = 271
F_MODEL = 272
F_AUTHOR = 315
F_COPYRIGHT = 33432
F_COMMENT = 40092
F_ISO = 34855
F_DATE = 36867