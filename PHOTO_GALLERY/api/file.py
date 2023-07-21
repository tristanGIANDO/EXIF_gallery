
import os
from PIL import Image
from PIL.ExifTags import TAGS

"""
Choisir version
Marqueur sur image
"""
class File(object):
    def __init__(self, path):

        if not os.path.isfile(path):
            raise FileNotFoundError(f"{path} is not a file.")
        
        self._name = os.path.basename(path)
        self._source = path
        self._data = self.read_image(path)

    def read_image(self, image_path):
        data = {}
        exif_info = self.get_exif_data(image_path)
        if exif_info:
            for tag, value in exif_info.items():
                data[tag] = value

        return data

    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
        return self._name
    
    def get_source(self):
        return self._source
    
    def set_source(self, source):
        self._source = source
        return self._source
    
    def get_author_from_data(self):
        return self._data.get("Artist", "")
    
    def set_author(self, author):
        self._data["Artist"] = author
    
    def get_comment_from_data(self):
        return self._data.get("XPComment", "")
    
    def set_comment(self, comment):
        self._data["XPComment"] = comment

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
        
    def save(self, data):
        with open("C:\\.database.json", "w") as file:
            file.write(data)