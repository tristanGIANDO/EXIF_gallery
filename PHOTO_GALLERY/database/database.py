import os, json
from database.data_file import DataFile

"""
{
    "files" : [
        {
            "_key" : "xxxx",
            "_name" : "example",
            "_version" : 1
        }
    ],
    "workspaces" : [
        "astro",
        "animals"
    ]
}
"""

class Database(object):
    def __init__(self, path:str):
        self._server = path
        self._data = self.read()
   
    def __repr__(self) -> str:
        return f"{self.__class__.__name__} : {self._server}"

    def read(self):
        if os.path.isfile(self._server):
            with open(self._server, 'r') as f:
                return json.load(f)
        else:
            return {}
        
    def get_files(self):
        files = []
        for file_data in self.read().get("files", []):
            files.append(DataFile(self._server, file_data))

        return files

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
        with open(self._server, "w") as f:
            json.dump(self._data, f, indent=4)

    def create_file(self, key:str, image:str, path:str=None, name:str=None, author:str=None, comment:str=None):
        file = DataFile(self._server)
        if file.create(key, image, name=name, path=path, author=author, comment=comment):
            if not "files" in self._data:
                self._data["files"] = []
            self._data["files"].append(file.read())

            return file
        else:
            print("File already exists.")