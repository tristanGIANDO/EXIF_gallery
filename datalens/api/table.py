from datalens.api import envs

class Table(object):
    def __init__(self, server) -> None:
        self._server = server
        self._cursor = server.cursor(buffered=True)
        self._name = ""

        self.create()

    def _exists(self) ->bool:
        self._cursor.execute("SHOW TABLES")
        for x in self._cursor:
            if x[0] == self._name:
                return True
            
    def _row_exists(self, row_id:str) ->bool:
        for row in self.select_rows():
            if row[0] == row_id:
                return True
            
    def create(self):
        if not self._exists():
            data = f"( \
                {envs.ID} VARCHAR(30)\
                )"

            request = f"CREATE TABLE {self._name} {data}"
            self._cursor.execute(request)

    def delete(self):
        request = f"DROP TABLE {self._name}"
        self._cursor.execute(request)

    def insert_into(self, data:dict):
        id = data.get(envs.ID)
        if self._row_exists(str(id)):
            return
        # id
        values = (id,)

        request = f"INSERT INTO {self._name} ({envs.ID}) VALUES (%s)"

        self._cursor.execute(request, values)
        self._server.commit()

    def select_rows(self):
        self._cursor.execute(f"SELECT * FROM {self._name}")
        return self._cursor.fetchall()
    
    def select_from_column(self, column:str, value:str):
        request = f"SELECT * FROM {self._name} WHERE {column} ='{value}'"
        self._cursor.execute(request)
        return self._cursor.fetchall()
    
    def update(self, column:str, id:str, new_value:str):
        try:
            sql = f"UPDATE {self._name} SET {column} = '{new_value}' WHERE ({envs.ID} = '{str(id)}')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            pass

    def delete_from(self, id:int):
        request = f"DELETE FROM {self._name} WHERE {envs.ID} = '{str(id)}'"
        self._cursor.execute(request)
        self._server.commit()