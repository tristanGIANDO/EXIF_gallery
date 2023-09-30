from datalens.api import envs

class FileTable(object):
    def __init__(self, server) -> None:
        self._server = server
        self._cursor = server.cursor(buffered=True)
        self._name = envs.ASTRO_FILE_TABLE_NAME

        self.create()

    def _exists(self) ->bool:
        self._cursor.execute("SHOW TABLES")
        for x in self._cursor:
            if x[0] == self._name:
                return True
            
    def _row_exists(self, row_id:str) ->bool:
        for file in self.select_rows():
            if file[0] == row_id:
                return True
            
    def create(self):
        pass

    def delete(self):
        sql = f"DROP TABLE {self._name}"
        self._cursor.execute(sql)

    def insert_into(self, data:dict):
        pass

    def select_rows(self):
        self._cursor.execute(f"SELECT * FROM {self._name}")
        return self._cursor.fetchall()
    
    def select_from_column(self, column:str, value:str):
        sql = f"SELECT * FROM {self._name} WHERE {column} ='{value}'"
        self._cursor.execute(sql)
        return self._cursor.fetchall()
    
    def get(self, column:str, id:str):
        sql = f"SELECT {column} FROM {self._name} WHERE {envs.ID} ='{id}'"
        self._cursor.execute(sql)
        return self._cursor.fetchall()
 
    def update(self, column:str, id:str, new_value:str):
        # global update
        try:
            sql = f"UPDATE {self._name} SET {column} = '{new_value}' WHERE ({envs.ID} = '{str(id)}')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            pass

    def delete_from(self, id:int, path:str):
        # delete from file table
        sql = f"DELETE FROM {self._name} WHERE {envs.ID} = '{str(id)}'"
        self._cursor.execute(sql)
        self._server.commit()