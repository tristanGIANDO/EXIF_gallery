import mysql.connector
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
  
  def connect(self, user, password):
    return mysql.connector.connect(
      host = "localhost",
      user = user,
      password = password,
      database = envs.DB_NAME
    )

  def _exists(self, file_table_name=None):
    self._cursor.execute("SHOW DATABASES")
    for x in self._cursor:
      if x[0] == file_table_name:
        return True
      
  def _table_exists(self, table=None):
    self._cursor.execute("SHOW TABLES")
    for x in self._cursor:
      if x[0] == table:
        return True
      
  def create(self):
    if not self._exists(envs.DB_NAME):
      self._cursor.execute(f"CREATE DATABASE {envs.DB_NAME}")
    else:
      print(f"{envs.DB_NAME} already exists.")

  def create_table(self, file_table_name):
    if not self._table_exists(file_table_name):
      columns = "("
      columns += "id INT AUTO_INCREMENT PRIMARY KEY," # auto increment db index but does not work, oh but it is for the table, not row
      columns += "name VARCHAR(45),"
      columns += "path VARCHAR(255)"
      columns += ")"

      self._cursor.execute(f"CREATE TABLE {file_table_name} {columns}")
      print("table created")
    else:
      print(f"{file_table_name} already exists.")

  def delete_table(self, table:str):
    request = f"DROP TABLE {table}"
    self._cursor.execute(request)

  # fileTable
  def add(self, values:list):
    request = f"INSERT INTO {envs.FILE_TABLE_NAME} (name, path) VALUES (%s,%s)"
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
  def remove_file(self, id):
    request = f"DELETE FROM {envs.FILE_TABLE_NAME} WHERE id = '{str(id)}'"
    self._cursor.execute(request)
    self._server.commit()

if __name__ == "__main__":
  import envs
  db = Database()
  # db.delete_table(envs.FILE_TABLE_NAME)
  db.add(["230521_IMG_7996_02", "C:/Users/giand/OneDrive/Images/@PORTFOLIO/230521_IMG_7996_02.jpg"])

  print(db.get_rows())