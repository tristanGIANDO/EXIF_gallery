import mysql.connector

DB_NAME = "photo_gallery"

class FileTable(object):
  def __init__(self, user:str="root", password:str="1969", table_name:str="file") -> None:
    self._user = user
    self._password = password

    self._server = self.connect(user, password)
    self._cursor = self._server.cursor()
    self._table = table_name
  
  def connect(self, user, password):
    return mysql.connector.connect(
      host = "localhost",
      user = user,
      password = password,
      database = DB_NAME
    )

  def exists(self):
    self._cursor.execute("SHOW TABLES")
    for x in self._cursor:
      if x[0] == self._table:
        return True
    
  # fileTable
  def add(self, values:tuple):
    request = f"INSERT INTO {self._table} (id, name, path) VALUES (%s,%s,%s)"
    self._cursor.execute(request, values)
    self._server.commit()

  # fileTable
  def get_rows(self):
    self._cursor.execute(f"SELECT * FROM {self._table}")
    return self._cursor.fetchall()
  
  # fileTable
  def get(self, column:str, value:str):
    request = f"SELECT * FROM {self._table} WHERE {column} ='{value}'"
    self._cursor.execute(request)
    return self._cursor.fetchall()
  
  # fileTable
  def delete(self, column:str, value:str):
    request = f"DELETE FROM {self._table} WHERE {column} = '{value}'"
    self._cursor.execute(request)
    self._server.commit()

if __name__ == "__main__":
  db = FileTable()
