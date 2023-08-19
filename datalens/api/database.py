import mysql.connector
from api import envs
from api.file_table import FileTable
from api.user_table import UserTable

class Database(object):
  def __init__(self, user:str="root", password:str="1969") -> None:
    self._user = user
    self._password = password
    self._name = envs.DB_NAME

    self._server = mysql.connector.connect(
      host = "localhost",
      user = user,
      password = password)
    self._cursor = self._server.cursor()
    
    self.create()

    self._server = self.connect(user, password)
    self._cursor = self._server.cursor()

    # init database
    self._files = FileTable(self._server)
    self._user = UserTable(self._server)
  
  def connect(self, user:str, password:str):
    return mysql.connector.connect(
      host = "localhost",
      user = user,
      password = password,
      database = self._name
    )

  def _exists(self) ->bool:
    self._cursor.execute("SHOW DATABASES")
    for x in self._cursor:
      if x[0] == self._name:
        return True
      
  def create(self):
    if not self._exists():
      self._cursor.execute(f"CREATE DATABASE {self._name}")