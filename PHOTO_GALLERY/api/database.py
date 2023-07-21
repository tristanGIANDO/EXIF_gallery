import os, json

class Database(object):
    def __init__(self, path:str):
        self._path = path
        self._files = []

        if os.path.isfile(self._path):
            self._files = self.read()
        
        self.save()

    def read(self):
        with open(self._path, 'r') as f:
            return json.load(f)

    def patch_data(self, data:dict):
        if not isinstance(data, dict):
            data = dict(data)
        index = len(self._files) + 1

        for image_data in self._files:
            if image_data.get("key", "") == index:
                self._files.remove(image_data)

        data["key"] = index
        self._files.append(data)
        
    def save(self):
        with open(self._path, "w") as f:
            json.dump(self._files, f, indent=4)