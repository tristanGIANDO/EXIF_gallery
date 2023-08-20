import traceback, os
from pathlib import Path
from api import envs, api_utils

class FileTable(object):
    def __init__(self, server) -> None:
        self._server = server
        self._cursor = server.cursor(buffered=True)
        self._name = envs.FILE_TABLE_NAME

        self.create()

    def _exists(self) ->bool:
        self._cursor.execute("SHOW TABLES")
        for x in self._cursor:
            if x[0] == self._name:
                return True
            
    def _row_exists(self, row_id:str) ->bool:
        for file in self.select_rows():
            if file[0] == row_id:
                return True
            
    def create(self):
        if not self._exists():
            data = f"( \
                {envs.ID} VARCHAR(30),\
                {envs.PATH} VARCHAR(250),\
                {envs.SUBJECT} VARCHAR(45),\
                {envs.ALBUM} VARCHAR(100),\
                {envs.MAKE} VARCHAR(45),\
                {envs.MODEL} VARCHAR(45),\
                {envs.MOUNT} VARCHAR(45),\
                {envs.FOCAL} INT(6),\
                {envs.F_NUMBER} VARCHAR(3),\
                {envs.ISO} INT(5),\
                {envs.LIGHTS} INT(5),\
                {envs.EXPOSURE_TIME} VARCHAR(10),\
                {envs.TOTAL_TIME} VARCHAR(10),\
                {envs.LOCATION} VARCHAR(70),\
                {envs.BORTLE} INT(1),\
                {envs.MOON_PHASE} INT(1),\
                {envs.SOFTWARE} VARCHAR(20),\
                {envs.AUTHOR} VARCHAR(25),\
                {envs.COMMENT} VARCHAR(255),\
                {envs.DATE} VARCHAR(25),\
                {envs.PATH_BRUT} VARCHAR(250)\
                )"

            request = f"CREATE TABLE {self._name} {data}"
            self._cursor.execute(request)

    def delete(self):
        request = f"DROP TABLE {self._name}"
        self._cursor.execute(request)

    def insert_into(self, data:dict):
        id = data.get(envs.ID)
        if self._row_exists(str(id)):
            return
        # id
        values = (id,)

        # path
        path = self.conform_file(data.get(envs.PATH), id)
        if not path:
            return
        values += (path,)

        # subject
        values += (data.get(envs.SUBJECT, ""),)

        # album
        values += (data.get(envs.ALBUM, ""),)

        # make
        values += (data.get(envs.MAKE, ""),)

        # model
        values += (data.get(envs.MODEL, ""),)

        # mount
        values += (data.get(envs.MOUNT, ""),)

        # focal
        values += (int(data.get(envs.FOCAL, 0)),)

        # aperture
        values += (data.get(envs.F_NUMBER, 0),)

        # iso
        values += (data.get(envs.ISO, 0),)

        # lights
        lights = data.get(envs.LIGHTS, 0)
        values += (lights,)

        # exposure time
        exposure = data.get(envs.EXPOSURE_TIME, 0)
        values += (exposure,)

        # total time
        values += (api_utils.convert_minutes_to_datetime(lights * exposure / 60),)

        # location
        values += (data.get(envs.LOCATION, ""),)
        # bortle
        values += (data.get(envs.BORTLE, 0),)
        # moon
        values += (api_utils.get_moon_phase(data.get(envs.DATE)),)
        # software
        values += (data.get(envs.SOFTWARE, ""),)
        # author
        values += (data.get(envs.AUTHOR, ""),)
        # comment
        values += (data.get(envs.COMMENT, ""),)
        # date
        values += (data.get(envs.DATE),)
        # brut
        brut = self.conform_file(data.get(envs.PATH_BRUT, ""), id)
        if not brut:
            brut = ""
        values += (brut,)

        request = f"INSERT INTO {self._name} \
        ({envs.ID},{envs.PATH},{envs.SUBJECT}, \
        {envs.ALBUM},{envs.MAKE},{envs.MODEL}, \
        {envs.MOUNT},{envs.FOCAL},{envs.F_NUMBER}, \
        {envs.ISO},{envs.LIGHTS},{envs.EXPOSURE_TIME}, \
        {envs.TOTAL_TIME},{envs.LOCATION},{envs.BORTLE}, \
        {envs.MOON_PHASE},{envs.SOFTWARE},{envs.AUTHOR}, \
        {envs.COMMENT},{envs.DATE},{envs.PATH_BRUT} \
        ) VALUES (%s,%s,%s,\
            %s,%s,%s,\
                %s,%s,%s,\
                    %s,%s,%s,\
                        %s,%s,%s,\
                            %s,%s,%s,\
                                %s,%s,%s)"

        self._cursor.execute(request, values)
        self._server.commit()

    # fileTable
    def select_rows(self):
        self._cursor.execute(f"SELECT * FROM {self._name}")
        return self._cursor.fetchall()
    
    # fileTable
    def select_from_column(self, column:str, value:str):
        request = f"SELECT * FROM {self._name} WHERE {column} ='{value}'"
        self._cursor.execute(request)
        return self._cursor.fetchall()
    
    # fileTable
    def update(self, column:str, id:str, new_value:str):
        # global update
        try:
            sql = f"UPDATE {self._name} SET {column} = '{new_value}' WHERE ({envs.ID} = '{str(id)}')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            pass

        if column == envs.LIGHTS or column == envs.EXPOSURE_TIME:
            self._update_total_time(str(id))
        elif column == envs.DATE:
            self._update_moon_phase(new_value, str(id))
    
    # fileTable
    def delete_from(self, id:int, path:str):
        request = f"DELETE FROM {self._name} WHERE {envs.ID} = '{str(id)}'"
        self._cursor.execute(request)
        self._server.commit()

        path = Path(path)
        os.remove(path)
        os.remove(path.parent / (path.stem + envs.IMAGE_SMALL_SUFFIX + path.suffix))
    
    def _update_total_time(self, id:str):
        # get epxosure total time
        request = f"SELECT {envs.LIGHTS},{envs.EXPOSURE_TIME} FROM {self._name} WHERE {envs.ID} = '{id}'"
        self._cursor.execute(request)
        result = self._cursor.fetchall()
        total_time = api_utils.convert_minutes_to_datetime(int(result[0][0]) * int(result[0][1]) / 60)

        try:
            sql = f"UPDATE {self._name} SET {envs.TOTAL_TIME} = '{total_time}' WHERE ({envs.ID} = '{id}')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            print(traceback.print_exc())

    def _update_moon_phase(self, date, id:str):
        moon_phase = api_utils.get_moon_phase(date)

        try:
            sql = f"UPDATE {self._name} SET {envs.MOON_PHASE} = '{moon_phase}' WHERE ({envs.ID} = '{id}')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            print(traceback.print_exc())

    def conform_file(sekf, path, id):
        if not os.path.isfile(path):
            return
        image_large_path = api_utils.copy_file(path, id)
        image_small_path = api_utils.resize_image(image_large_path, 300, 200)

        return image_large_path