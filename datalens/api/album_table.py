from datalens.api import envs
from datalens.api.table import Table
import os,shutil

class AlbumTable(Table):
    def __init__(self, server) -> None:
        super().__init__(server)
        self._server = server
        self._cursor = server.cursor(buffered=True)
        self._name = envs.ALBUM_TABLE_NAME

        self.create()
            
    def create(self):
        if not self._exists():
            data = f"( \
                {envs.ID} INT AUTO_INCREMENT PRIMARY KEY,\
                {envs.ALBUM_NAME} VARCHAR(45),\
                {envs.ALBUM_TYPE} VARCHAR(45)\
                )"

            request = f"CREATE TABLE {self._name} {data}"
            self._cursor.execute(request)

    def insert_into(self, data:dict):
        # first name
        values = (data.get(envs.ALBUM_NAME, ""),)

        # last name
        values += (data.get(envs.ALBUM_TYPE, ""),)

        request = f"INSERT INTO {self._name} \
        ({envs.ALBUM_NAME},{envs.ALBUM_TYPE}) VALUES (%s,%s)"

        self._cursor.execute(request, values)
        self._server.commit()

    def delete_album(self, album_name):
        request = f"DELETE FROM {self._name} WHERE {envs.ALBUM_NAME} = '{album_name}'"
        self._cursor.execute(request)
        self._server.commit()

        request = f"DELETE FROM {envs.FILE_TABLE_NAME} WHERE {envs.ALBUM} = '{album_name}'"
        self._cursor.execute(request)
        self._server.commit()

        path = os.path.join(envs.ROOT, album_name)
        if os.path.isdir(path):
            shutil.rmtree(path)