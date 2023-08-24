from datalens.api import envs
from datalens.api.table import Table

class UserTable(Table):
    def __init__(self, server) -> None:
        super().__init__(server)
        self._server = server
        self._cursor = server.cursor(buffered=True)
        self._name = envs.USER_TABLE_NAME

        self.create()
            
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

            request = f"CREATE TABLE {self._name} {data}"
            self._cursor.execute(request)

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

        request = f"INSERT INTO {self._name} \
        ({envs.ID},{envs.FIRST_NAME},{envs.LAST_NAME},{envs.DESC},{envs.PATH}) VALUES (%s,%s,%s,%s,%s)"

        self._cursor.execute(request, values)
        self._server.commit()
    
    def update(self, column:str, new_value:str):
        try:
            sql = f"UPDATE {self._name} SET {column} = '{new_value}' WHERE ({envs.ID} = '0')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            pass