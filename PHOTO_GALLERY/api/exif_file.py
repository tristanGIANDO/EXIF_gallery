import os
from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path

from api import envs

class ExifFile(object):
    def __init__(self, path):
        path = Path(path)
        if not path.is_file():
            raise FileNotFoundError(f"{path} is not a file.")
        
        self._path = path
        self._data = self.from_data()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} : {self._path}"

    def from_data(self):
        data = {}

        # add custom data
        data[envs.F_KEY] = os.stat(self._path).st_ino
        data[envs.F_NAME] = os.path.splitext(os.path.basename(self._path))[0]
        data[envs.F_PATH] = self._path
        
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
        return self._data.get(envs.F_KEY,"")
    
    def get_name(self) ->str:
        return self._data.get(envs.F_NAME,"")
    
    def get_path(self) ->str:
        return self._path
    
    def get_author(self) ->str:
        return self._data.get(envs.F_AUTHOR, "")
    
    def get_comment(self) ->str:
        return self._data.get(envs.F_COMMENT, "")
    
    def get_image(self) ->str:
        return self._data.get(envs.F_IMAGE, "")
    
    def get_description(self) ->str:
        return self._data.get(envs.F_DESCRIPTION,"")
    
    def get_camera(self) ->str:
        camera = self._data.get(envs.F_MAKE)
        model = self._data.get(envs.F_MODEL)
        if camera and model:
            return f"{camera} {model}"
    
    def get_iso(self) ->int:
        return self._data.get(envs.F_ISO, 0)
    
    def get_date(self) ->str:
        return self._data.get(envs.F_DATE, "")
    