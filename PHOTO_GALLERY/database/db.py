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
    # columns
    if not self.file_exists(file_name):
      columns = "("
      columns += "id INT AUTO_INCREMENT PRIMARY KEY," # auto increment db index
      columns += "name VARCHAR(45),"
      columns += "path VARCHAR(255)"
      columns += ")"

      self._server.execute(f"CREATE TABLE {file_name} {columns}")
    else:
      print(f"{file_name} already exists.")

  def file_exists(self, file_name=None):
    self._cursor.execute("SHOW TABLES")
    for x in self._cursor:
      if x[0] == file_name:
        return True
      
  def add(self, table:str, values:tuple):
    request = f"INSERT INTO {table} (id, name, path) VALUES (%s,%s,%s)"

    self._cursor.execute(request, values)
    self._server.commit()

  def get_rows(self, table:str):
    self._cursor.execute(f"SELECT * FROM {table}")

    return self._cursor.fetchall()

if __name__ == "__main__":
  db = Database()
  db.add("file", ("1", "example.jpg", "path/file"))
  print(db.get_rows("file"))