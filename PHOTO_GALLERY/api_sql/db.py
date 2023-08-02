import mysql.connector, os
from api_sql import envs, db_utils

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
        {envs.ID} VARCHAR(30),\
        {envs.PATH} VARCHAR(250),\
        {envs.SUBJECT} VARCHAR(45),\
        {envs.DESC} VARCHAR(100),\
        {envs.CAMERA} VARCHAR(45),\
        {envs.MOUNT} VARCHAR(45),\
        {envs.FOCAL} INT(4),\
        {envs.APERTURE} VARCHAR(3),\
        {envs.ISO} INT(5),\
        {envs.LIGHTS} INT(5),\
        {envs.EXPOSURE_TIME} INT(4),\
        {envs.TIME} VARCHAR(10),\
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

    # path
    values += (db_utils.copy_file(data.get(envs.PATH), id),)

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
    lights = int(data.get(envs.LIGHTS, 0))
    values += (lights,)

    # exposure time
    exposure = int(data.get(envs.EXPOSURE_TIME, 0))
    values += (exposure,)

    # total time
    values += (db_utils.convert_minutes_to_datetime(lights * exposure / 60),)

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
    # global update
    try:
      sql = f"UPDATE {envs.FILE_TABLE_NAME} SET {column} = '{new_value}' WHERE ({envs.ID} = '{str(id)}')"
      self._cursor.execute(sql)
      self._server.commit()
    except:
      pass
    # update total time
    if column == "lights" or column == "exposure":
      time_in_minutes = self.get_exposure_total_time(id)
      total_time = db_utils.convert_minutes_to_datetime(time_in_minutes)
      try:
        sql = f"UPDATE {envs.FILE_TABLE_NAME} SET time = '{total_time}' WHERE ({envs.ID} = '{str(id)}')"
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

  def get_exposure_total_time(self, id:int):
    request = f"SELECT lights,exposure FROM {envs.FILE_TABLE_NAME} WHERE {envs.ID} = '{str(id)}'"
    self._cursor.execute(request)
    result = self._cursor.fetchall()
    return result[0][0] * result[0][1] / 60

if __name__ == "__main__":
  import envs
  id = 3377699720531883
  db = Database()
  request = f"SELECT lights,exposure FROM {envs.FILE_TABLE_NAME} WHERE {envs.ID} = '{str(id)}'"
  db._cursor.execute(request)
  result = db._cursor.fetchall()
  time = result[0][0] * result[0][1] / 60
  print(time)

