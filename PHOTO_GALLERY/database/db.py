import mysql.connector

DB_NAME = "photo_gallery"

class Database(object):
  def __init__(self, user:str="root", password:str="1969") -> None:
    self._user = user
    self._password = password

    self._server = self.connect(user, password)
    self._cursor = self._server.cursor()
  
  def connect(self, user, password):
    return mysql.connector.connect(
      host = "localhost",
      user = user,
      password = password,
      database = DB_NAME
    )

  def create(self):
    if not self.exists(DB_NAME):
      self._server.execute(f"CREATE DATABASE {DB_NAME}")
    else:
      print(f"{DB_NAME} already exists.")

  def exists(self, db_name=None):
    self._cursor.execute("SHOW DATABASES")
    for x in self._cursor:
      if x[0] == db_name:
        return True

  def create_file(self, file_name):
    if not self.table_exists(file_name):
      columns = "("
      columns += "id INT AUTO_INCREMENT PRIMARY KEY," # auto increment db index but does not work, oh but it is for the table, not row
      columns += "name VARCHAR(45),"
      columns += "path VARCHAR(255)"
      columns += ")"

      self._server.execute(f"CREATE TABLE {file_name} {columns}")
    else:
      print(f"{file_name} already exists.")

  def table_exists(self, table=None):
    self._cursor.execute("SHOW TABLES")
    for x in self._cursor:
      if x[0] == table:
        return True
    
  # fileTable
  def add(self, table:str, values:tuple):
    request = f"INSERT INTO {table} (id, name, path) VALUES (%s,%s,%s)"
    self._cursor.execute(request, values)
    self._server.commit()

  # fileTable
  def get_rows(self, table:str):
    self._cursor.execute(f"SELECT * FROM {table}")
    return self._cursor.fetchall()
  
  # fileTable
  def get(self, table:str, column:str, value:str):
    request = f"SELECT * FROM {table} WHERE {column} ='{value}'"
    self._cursor.execute(request)
    return self._cursor.fetchall()
  
  # fileTable
  def delete(self, table:str, column:str, value:str):
    request = f"DELETE FROM {table} WHERE {column} = '{value}'"
    self._cursor.execute(request)
    self._server.commit()

  def delete_table(self, table:str):
    request = f"DROP TABLE {table}"
    self._cursor.execute(request)

if __name__ == "__main__":
  db = Database()
  db.add("file", ("1", "example.jpg", "path/file"))
  print(db.delete_table("file"))