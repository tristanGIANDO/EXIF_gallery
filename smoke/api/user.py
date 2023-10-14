from smoke.api import envs

class UserTable(object):
    def __init__(self, server) -> None:
        self._server = server
        self._cursor = server.cursor(buffered=True)
        self._name = envs.USER_TABLE_NAME

        self.create()

    def _exists(self) ->bool:
        self._cursor.execute("SHOW TABLES")
        for x in self._cursor:
            if x[0] == self._name:
                return True
            
    def get_user(self) ->list:
        user = self.select_rows()
        if user:
            return user[0]
            
    def create(self):
        if not self._exists():
            data = f"( \
                {envs.ID} VARCHAR(1),\
                {envs.FIRST_NAME} VARCHAR(30),\
                {envs.LAST_NAME} VARCHAR(250),\
                {envs.DESC} VARCHAR(100),\
                {envs.PATH} VARCHAR(255)\
                )"

            sql = f"CREATE TABLE {self._name} {data}"
            self._cursor.execute(sql)

    def delete(self):
        sql = f"DROP TABLE {self._name}"
        self._cursor.execute(sql)

    def insert_into(self, data:dict):
        values = ("0",)
        # first name
        values += (data.get(envs.FIRST_NAME, ""),)

        # last name
        values += (data.get(envs.LAST_NAME, ""),)

        # description
        values += (data.get(envs.DESC, ""),)

        # thumbnail
        values += (data.get(envs.PATH, ""),)

        sql = f"INSERT INTO {self._name} \
        ({envs.ID},{envs.FIRST_NAME},{envs.LAST_NAME},{envs.DESC},{envs.PATH}) VALUES (%s,%s,%s,%s,%s)"

        self._cursor.execute(sql, values)
        self._server.commit()

    def select_rows(self):
        self._cursor.execute(f"SELECT * FROM {self._name}")
        return self._cursor.fetchall()
    
    def select_from_column(self, column:str, value:str):
        sql = f"SELECT * FROM {self._name} WHERE {column} ='{value}'"
        self._cursor.execute(sql)
        return self._cursor.fetchall()
    
    def update(self, column:str, new_value:str):
        try:
            sql = f"UPDATE {self._name} SET {column} = '{new_value}' WHERE ({envs.ID} = '0')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            pass