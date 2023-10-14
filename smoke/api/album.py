from smoke.api import envs
from smoke.api import astro
import os,shutil

class AlbumTable(object):
    def __init__(self, server) -> None:
        self._server = server
        self._cursor = server.cursor(buffered=True)
        self._name = envs.ALBUM_TABLE_NAME

        self.create()

    def _exists(self) ->bool:
        self._cursor.execute("SHOW TABLES")
        for x in self._cursor:
            if x[0] == self._name:
                return True
            
    def _row_exists(self, row_id:str) ->bool:
        for album in self.select_rows():
            if album[0] == row_id:
                return True
            
    def create(self):
        if not self._exists():
            data = f"( \
                {envs.ID} INT AUTO_INCREMENT PRIMARY KEY,\
                {envs.ALBUM_NAME} VARCHAR(45),\
                {envs.ALBUM_TYPE} VARCHAR(45)\
                )"

            sql = f"CREATE TABLE {self._name} {data}"
            self._cursor.execute(sql)

    def delete(self):
        sql = f"DROP TABLE {self._name}"
        self._cursor.execute(sql)

    def insert_into(self, data:dict):
        # first name
        values = (data.get(envs.ALBUM_NAME, ""),)

        # last name
        values += (data.get(envs.ALBUM_TYPE, ""),)

        sql = f"INSERT INTO {self._name} \
        ({envs.ALBUM_NAME},{envs.ALBUM_TYPE}) VALUES (%s,%s)"

        self._cursor.execute(sql, values)
        self._server.commit()

    def get_type(self, name:str):
        sql = f"SELECT {envs.ALBUM_TYPE} FROM {self._name} WHERE {envs.ALBUM_NAME} ='{name}'"
        self._cursor.execute(sql)
        return self._cursor.fetchall()[0][0]
    
    def select_rows(self):
        self._cursor.execute(f"SELECT * FROM {self._name}")
        return self._cursor.fetchall()

    def select_from_column(self, column:str, value:str):
        sql = f"SELECT * FROM {self._name} WHERE {column} ='{value}'"
        self._cursor.execute(sql)
        return self._cursor.fetchall()

    def update(self, column:str, id:str, new_value:str):
        try:
            sql = f"UPDATE {self._name} SET {column} = '{new_value}' WHERE ({envs.ID} = '{str(id)}')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            pass

    def delete_album(self, album_name):
        # delete album from album table
        sql = f"DELETE FROM {self._name} WHERE {envs.ALBUM_NAME} = '{album_name}'"
        self._cursor.execute(sql)
        self._server.commit()

        # delete files from os
        self._cursor.execute(f"SELECT {envs.PATH} FROM {envs.ASTRO_FILE_TABLE_NAME} WHERE {envs.ALBUM} = '{album_name}'")
        files = self._cursor.fetchall()
        print(files)
        if files:
            for file in files[0]:
                path = os.path.dirname(file)
                if os.path.dirname(path):
                    shutil.rmtree(path)

        # delete files from version table
        self._cursor.execute(f"SELECT {envs.ID} FROM {envs.ASTRO_FILE_TABLE_NAME} WHERE {envs.ALBUM} = '{album_name}'")
        files = self._cursor.fetchall()
        if files:
            for id in files[0]:
                sql = f"DELETE FROM {envs.VERSION_TABLE_NAME} WHERE {envs.VERSION_PARENT_ID} = '{str(id)}'"
                self._cursor.execute(sql)
                self._server.commit()
    
        # delete files from album table
        sql = f"DELETE FROM {envs.ASTRO_FILE_TABLE_NAME} WHERE {envs.ALBUM} = '{album_name}'"
        self._cursor.execute(sql)
        self._server.commit()
        