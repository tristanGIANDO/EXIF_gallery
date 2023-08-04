from pathlib import Path

DB_NAME = "db01"
FILE_TABLE_NAME = "files"

ROOT = Path.home() / ".database"

ID = "id"
PATH = "path"
SUBJECT = "subject"
DESC = "description"
MAKE = "make"
MODEL = "model"
MOUNT = "mount"
FOCAL = "focal"
F_NUMBER = "fNumber"
ISO = "iso"
LIGHTS = "lights"
EXPOSURE_TIME = "exposureTime"
TOTAL_TIME = "totalTime"
LOCATION = "location"
BORTLE = "bortle"
MOON_PHASE = "moonPhase"
SOFTWARE = "software"
AUTHOR = "author"
COMMENT = "comment"
DATE = "date"
PATH_BRUT = "brutPath"

EXIF_TO_DATABASE_MAPPING = {
        270 : DESC,
        271 : MAKE, # "NIKON CORPORATION"
        272 : MODEL, # "NIKON D810"
        315 : AUTHOR,
        40092 : COMMENT,
        34855 : ISO,
        306 : DATE, #"2016:10:20 12:22:49"
        36867 : DATE, #"2016:01:29 12:53:01"
        37386 : FOCAL, # "85.0"
        33434 : EXPOSURE_TIME, #"0.004"
        33437 : F_NUMBER,
        # 42036 : MODEL_LENS, # "85.0 mm f/1.8"
        305 : SOFTWARE, #"Adobe Photoshop CC 2015.5 (Macintosh)"
        # 37385 : FLASH #"16"
    }

IMAGE_SMALL_SUFFIX = "-small"