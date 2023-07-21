import os, json
from PIL import Image
from PIL.ExifTags import TAGS

"""
Choisir version
Marqueur sur image
"""
class ExifFile(object):
    def __init__(self, path):

        if not os.path.isfile(path):
            raise FileNotFoundError(f"{path} is not a file.")
        
        self._path = path
        self._data = self.read_image(path)
        
        self.set_path(path)

    def read_image(self, image_path):
        data = {}
        exif_info = self.get_exif_data(image_path)
        if exif_info:
            for tag, value in exif_info.items():
                data[tag] = value

        return data

    def get_name(self):
        return os.path.splitext(os.path.basename(self._path))[0]
    
    def set_name(self, name):
        self._data["name"] = name
    
    def get_path(self):
        return self._data.get("path","")
    
    def set_path(self, path):
        self._data["path"] = path
    
    def get_author(self):
        return self._data.get("Artist", "")
    
    def get_comment(self):
        return self._data.get("XPComment", "")
    
    def convert_bytes_to_str(self, data):
        if isinstance(data, bytes):
            try:
                return data.decode('utf-8')
            except UnicodeDecodeError:
                return "Unable to decode"
        return data

    def get_exif_data(self, image_path):
        try:
            with Image.open(image_path) as img:
                exif_data = img._getexif()

                if exif_data is not None:
                    exif_info = {}
                    for tag, value in exif_data.items():
                        tag_name = TAGS.get(tag, tag)
                        exif_info[tag_name] = self.convert_bytes_to_str(value)
                    return exif_info
                else:
                    return None
        except Exception as e:
            print(f"Error while getting EXIF data : {e}")
            return None