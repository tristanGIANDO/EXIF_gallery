import os, json
from PIL import Image
from PIL.ExifTags import TAGS

from api import envs

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
        data[envs.KEY] = os.stat(self._path).st_ino
        data[envs.NAME] = os.path.splitext(os.path.basename(self._path))[0]
        data[envs.PATH] = self._path
        
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

        # convert image to bytes
        # with open(self._path, 'rb') as image_file:
        #     bytes_data = image_file.read()
        #     data[envs.IMAGE] = bytes_data

        return data
    
    def read(self):
        return self._data
                
    def get_id(self):
        return self._data.get(envs.KEY,"")
    
    def get_name(self):
        return self._data.get(envs.NAME,"")
    
    def get_path(self):
        return self._path
    
    def get_author(self):
        return self._data.get(envs.AUTHOR, "")
    
    def get_comment(self):
        return self._data.get(envs.COMMENT, "")
    
    def get_image(self):
        return self._data.get(envs.IMAGE, "")