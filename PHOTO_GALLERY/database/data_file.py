from image.exif_file import ExifFile
import json
from database import envs

class DataFile(object):
    def __init__(self, server, data):
        
        self._server = server
        self._base = exif_file
        self._data = {}

    def get_all(self):
        with open(self._server, 'r') as f:
            return json.load(f).get("files", [])
    
    def exists(self, key):
        for k in list(self.get_all().keys()):
            if k == key:
                return True
        else:
            return False

    def modify(self):
        pass

    def create(self, key:str, name:str=None, author:str=None, comment:str=None):
        if not self.exists(self._base.get_key()):
            self.set_key(key)
            if name:
                self.set_name(name)
            if author:
                self.set_author(author)
            if comment:
                self.set_comment(comment)

        return self._data

    def get_key(self):
        return self._data.get(envs.KEY,"")
    
    def set_key(self, key):
        self._data[envs.KEY] = key
    
    def get_name(self):
        return self._data.get(envs.NAME,"")
    
    def set_name(self, name):
        self._data[envs.NAME] = name
    
    def get_path(self):
        return self._path
    
    def set_path(self,path):
        self._data[envs.PATH] = path
    
    def get_comment(self):
        return self._data.get(envs.COMMENT, "")
    
    def set_comment(self, comment):
        self._data[envs.COMMENT] = comment

    def get_author(self):
        return self._data.get(envs.AUTHOR, "")
    
    def set_author(self, author):
        self._data[envs.AUTHOR] = author