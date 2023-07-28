import mysql.connector, os, shutil
from api_sql import envs

class Database(object):
  def __init__(self, user:str="root", password:str="1969") -> None:
    self._user = user
    self._password = password

    self._server = mysql.connector.connect(
      host = "localhost",
      user = user,
      password = password)
    self._cursor = self._server.cursor()
    
    self.create()

    self._server = self.connect(user, password)
    self._cursor = self._server.cursor()

    # init database
    
    self.create_table(envs.FILE_TABLE_NAME)
  
  def connect(self, user:str, password:str):
    return mysql.connector.connect(
      host = "localhost",
      user = user,
      password = password,
      database = envs.DB_NAME
    )

  def _exists(self, file_table_name:str=None) ->bool:
    self._cursor.execute("SHOW DATABASES")
    for x in self._cursor:
      if x[0] == file_table_name:
        return True
      
  def _table_exists(self, table:str=None) ->bool:
    self._cursor.execute("SHOW TABLES")
    for x in self._cursor:
      if x[0] == table:
        return True
      
  def _row_exists(self, row_id:int) ->bool:
    for file in self.get_rows():
      if file[0] == str(row_id):
        return True
      
  def create(self):
    if not self._exists(envs.DB_NAME):
      self._cursor.execute(f"CREATE DATABASE {envs.DB_NAME}")
    else:
      print(f"{envs.DB_NAME} already exists.")

  def create_table(self, file_table_name):
    if not self._table_exists(file_table_name):
      data = f"( \
        id VARCHAR(20), \
        {envs.NAME} VARCHAR(45), \
        {envs.PATH} VARCHAR(255), \
        {envs.AUTHOR} VARCHAR(45), \
        {envs.COMMENT} VARCHAR(255) \
        )"

      self._cursor.execute(f"CREATE TABLE {file_table_name} {data}")
      print("table created")
    else:
      print(f"{file_table_name} already exists.")

  def delete_table(self, table:str):
    request = f"DROP TABLE {table}"
    self._cursor.execute(request)

  # fileTable
  def add(self, data:dict):
    id = data.get("id")
    if self._row_exists(id):
      return
    # print(data)
    # id
    values = (id,)
    # name
    values += (data.get(envs.NAME, None),)
    # path
    path = data.get(envs.PATH)
    if os.path.isfile(path):
      if not os.path.isdir(envs.ROOT):
        os.mkdir(envs.ROOT)
      new_path = os.path.join(envs.ROOT, f"{id}{os.path.splitext(path)[-1]}")
      shutil.copy(path, new_path)
      values += (new_path,)
    # author
    values += (data.get(envs.AUTHOR, None),)
    # comment
    values += (data.get(envs.COMMENT, None),)

    request = f"INSERT INTO {envs.FILE_TABLE_NAME} (id,name,path,author,comment) VALUES (%s,%s,%s,%s,%s)"

    self._cursor.execute(request, values)
    self._server.commit()

  # fileTable
  def get_rows(self):
    self._cursor.execute(f"SELECT * FROM {envs.FILE_TABLE_NAME}")
    return self._cursor.fetchall()
  
  # fileTable
  def get(self, column:str, value:str):
    request = f"SELECT * FROM {envs.FILE_TABLE_NAME} WHERE {column} ='{value}'"
    self._cursor.execute(request)
    return self._cursor.fetchall()
  
  # fileTable
  def update(self, column:str, id:str, new_value:str):
    sql = f"UPDATE {envs.FILE_TABLE_NAME} SET {column} = '{new_value}' WHERE (id = '{str(id)}')"
    self._cursor.execute(sql)
    self._server.commit()
  
  # fileTable
  def remove_file(self, id, path):
    request = f"DELETE FROM {envs.FILE_TABLE_NAME} WHERE id = '{str(id)}'"
    self._cursor.execute(request)
    self._server.commit()

    os.remove(path)

if __name__ == "__main__":
  import envs
  db = Database()
  # db.delete_table(envs.FILE_TABLE_NAME)
  # db.add(["230521_IMG_7996_02", "C:/Users/giand/OneDrive/Images/@PORTFOLIO/230521_IMG_7996_02.jpg"])
  db.update("name", 7599824371229639, "nouveau nom")
  print(db.get_rows())