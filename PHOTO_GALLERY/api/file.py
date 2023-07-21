
import os

class File(object):
    def __init__(self, path):

        if not os.path.isfile(path):
            raise FileNotFoundError(f"{path} is not a file.")
        
        self._name = os.path.basename(path)
        self._source = path

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