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

  def create_table(self, file_table_name:str):
    if not self._table_exists(file_table_name):
      data = f"( \
        {envs.ID} VARCHAR(20),\
        {envs.PATH} VARCHAR(250),\
        {envs.SUBJECT} VARCHAR(20),\
        {envs.DESC} VARCHAR(100),\
        {envs.CAMERA} VARCHAR(20),\
        {envs.MOUNT} VARCHAR(30),\
        {envs.FOCAL} INT(4),\
        {envs.APERTURE} VARCHAR(3),\
        {envs.ISO} INT(5),\
        {envs.LIGHTS} INT(5),\
        {envs.EXPOSURE_TIME} INT(3),\
        {envs.TIME} VARCHAR(5),\
        {envs.PLACE} VARCHAR(50),\
        {envs.BORTLE} INT(1),\
        {envs.MOON} INT(2),\
        {envs.PROCESS} VARCHAR(20),\
        {envs.AUTHOR} VARCHAR(25),\
        {envs.COMMENT} VARCHAR(255),\
        {envs.DATE} VARCHAR(10)\
        )"

      request = f"CREATE TABLE {file_table_name} {data}"
      self._cursor.execute(request)

  def delete_table(self, table:str):
    request = f"DROP TABLE {table}"
    self._cursor.execute(request)

  # fileTable
  def add(self, data:dict):
    id = data.get(envs.ID)
    if self._row_exists(id):
      return
    # id
    values = (id,)

    # copy path
    path = data.get(envs.PATH)
    if os.path.isfile(path):
      if not os.path.isdir(envs.ROOT):
        os.mkdir(envs.ROOT)
      new_path = os.path.join(envs.ROOT, f"{id}{os.path.splitext(path)[-1]}")
      shutil.copy(path, new_path)
      values += (new_path,)

    # subject
    values += (data.get(envs.SUBJECT, "None"),)
    # description
    values += (data.get(envs.DESC, "None"),)
    # camera
    values += (data.get(envs.CAMERA, "None"),)
    # mount
    values += (data.get(envs.MOUNT, "None"),)
    # focal
    values += (int(data.get(envs.FOCAL, 0)),)
    # aperture
    values += (float(data.get(envs.APERTURE, 0.0)),)
    # iso
    values += (int(data.get(envs.ISO, 0)),)
    # lights
    values += (int(data.get(envs.LIGHTS, 0)),)
    # exposure time
    values += (int(data.get(envs.EXPOSURE_TIME, 0)),)
    # total time
    values += (0,)
    # place
    values += (data.get(envs.PLACE, "None"),)
    # bortle
    values += (int(data.get(envs.BORTLE, 0)),)
    # moon
    values += (int(data.get(envs.MOON, 0)),)
    # process
    values += (data.get(envs.PROCESS, "None"),)
    # author
    values += (data.get(envs.AUTHOR, "None"),)
    # comment
    values += (data.get(envs.COMMENT, "None"),)
    # date
    values += ("None",)

    request = f"INSERT INTO {envs.FILE_TABLE_NAME} \
      ({envs.ID},{envs.PATH},{envs.SUBJECT}, \
      {envs.DESC},{envs.CAMERA},{envs.MOUNT},{envs.FOCAL}, \
      {envs.APERTURE},{envs.ISO},{envs.LIGHTS},{envs.EXPOSURE_TIME}, \
      {envs.TIME},{envs.PLACE},{envs.BORTLE},{envs.MOON}, \
      {envs.PROCESS},{envs.AUTHOR},{envs.COMMENT},{envs.DATE} \
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

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
    try:
      sql = f"UPDATE {envs.FILE_TABLE_NAME} SET {column} = '{new_value}' WHERE ({envs.ID} = '{str(id)}')"
      self._cursor.execute(sql)
      self._server.commit()
    except:
      pass
  
  # fileTable
  def remove_file(self, id:int, path:str):
    request = f"DELETE FROM {envs.FILE_TABLE_NAME} WHERE {envs.ID} = '{str(id)}'"
    self._cursor.execute(request)
    self._server.commit()

    os.remove(path)

if __name__ == "__main__":
  import envs
  db = Database()
  db.update("name", 7599824371229639, "nouveau nom")
  print(db.get_rows())
