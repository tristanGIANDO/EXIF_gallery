import json, os
from database import envs

from PIL import Image
import io

class DataFile(object):
    def __init__(self, server, file_data=None):
        
        self._server = server
        if not file_data:
            self._data = {}
        else:
            self._data = self.from_data(file_data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} : {self._data}"

    def read(self):
        return self._data
    
    def read_database(self): #temp
        if os.path.isfile(self._server):
            with open(self._server, 'r') as f:
                return json.load(f)
        else:
            return {}
        
    def exists(self, key):
        for file in self.read_database().get("files", []):
            if file.get(envs.KEY) == key:
                return True
        else:
            return False

    def modify(self):
        pass

    def from_data(self, data):
        built_data = {}
        if isinstance(data, dict):
            key = data.get(envs.KEY, "")
            if not key:
                raise KeyError("Need a key, incompatible data.")
            built_data[envs.KEY] = key
            built_data[envs.IMAGE] = data.get(envs.IMAGE)
            built_data[envs.NAME] = data.get(envs.NAME)
            built_data[envs.AUTHOR] = data.get(envs.AUTHOR)
            built_data[envs.COMMENT] = data.get(envs.COMMENT)
            built_data[envs.PATH] = data.get(envs.PATH)

        return built_data

    def create(self, key:str, image:str, path:str=None, name:str=None, author:str=None, comment:str=None):
        if not self.exists(key):
            self.set_key(key)

            self.set_image(image)

            if path:
                self.set_path(path)
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

    def get_image(self):
        bytes_data = self._data.get(envs.IMAGE,"")
        if bytes_data:
            with io.BytesIO(eval(bytes_data)) as image_stream:
                image = Image.open(image_stream)
            return image

    def set_image(self, image):
        self._data[envs.IMAGE] = image
    
    def get_name(self):
        return self._data.get(envs.NAME,"")
    
    def set_name(self, name):
        self._data[envs.NAME] = name
    
    def get_path(self):
        return self._data.get(envs.PATH)
    
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