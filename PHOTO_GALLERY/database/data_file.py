from image.exif_file import ExifFile

class DataFile(object):
    def __init__(self, data):
        self._key = data.get("key","")
        self._name = data.get("name","")
        self._comment = data.get("comment","")
        self._author = data.get("author","")

    def get_key(self):
        return self._key
    
    def set_key(self, key):
        self._key = key
        return self._key
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
        return self._name
    
    def get_comment(self):
        return self._comment
    
    def set_comment(self, comment):
        self._comment = comment

    def get_author(self):
        return self._author
    
    def set_author(self, author):
        self._author = author