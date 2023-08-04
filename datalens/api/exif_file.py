import os
from PIL import Image
from PIL.ExifTags import TAGS

# exif conventions nomenclature
ID = "_key"
SUBJECT = "_name"
PATH = "_path"
IMAGE = "_image"
DESCRIPTION = 270
MAKE = 271
MODEL = 272
AUTHOR = 315
COPYRIGHT = 33432
COMMENT = 40092
ISO = 34855
DATE = 36867
DATE_LAST_MODIFIED = 306
WIDTH = 256
HEIGHT = 257
BITS_PER_SAMPLE =  258
COMPRESSION = 259
SOFTWARE = 305
COLORSPACE = 40961
EXPOSURE_TIME = 33434
APERTURE = 33437
FLASH = 37385
FOCAL = 37386

GPS = 34853
GPS_LAT = 0x0002
GPS_LON = 0x0004
GPS_ALT = 0x0006

# ShutterSpeedValue (Valeur de vitesse d'obturation) : TAG 37377
# ApertureValue (Valeur d'ouverture) : TAG 37378

class ExifFile(object):
    def __init__(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"{path} is not a file.")
        
        self._path = path
        self._data = self.from_data()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} : {self._path}"

    def from_data(self):
        data = {}

        # add custom data
        data[ID] = os.stat(self._path).st_ino
        data[SUBJECT] = os.path.splitext(os.path.basename(self._path))[0]
        data[PATH] = self._path
        
        # add exifs
        with Image.open(self._path) as img:
            exif_data = img._getexif()

            if exif_data:
                for tag, value in exif_data.items():
                    # tag_name = TAGS.get(tag, tag)
                    # decode bytes
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8')
                        except UnicodeDecodeError:
                            pass

                    data[tag] = value

        return data
    
    def read(self) ->dict:
        return self._data
                
    def get_id(self) ->str:
        return self._data.get(ID,"")
    
    def get_name(self) ->str:
        return self._data.get(SUBJECT,"")
    
    def get_path(self) ->str:
        return self._path
    
    def get_author(self) ->str:
        return self._data.get(AUTHOR, "")
    
    def get_comment(self) ->str:
        return self._data.get(COMMENT, "")
    
    def get_description(self) ->str:
        return self._data.get(DESCRIPTION,"")
    
    def get_camera(self) ->str:
        camera = self._data.get(MAKE)
        model = self._data.get(MODEL)
        if camera and model:
            return f"{camera} {model}"
    
    def get_iso(self) ->int:
        return self._data.get(ISO, 0)
    
    def get_date(self) ->str:
        return self._data.get(DATE, "")
    