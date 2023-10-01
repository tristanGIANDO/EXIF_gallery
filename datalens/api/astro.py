import traceback, os, shutil
from pathlib import Path
from PIL import Image
from datalens.api import envs, utils
from datalens.api.file import FileTable

class AstroFileTable(FileTable):
    def __init__(self, server) -> None:
        super().__init__(server)
        self._name = envs.ASTRO_FILE_TABLE_NAME

        self.create()
            
    def create(self):
        if not self._exists():
            data = f"( \
                {envs.ID} VARCHAR(30),\
                {envs.PATH} VARCHAR(250),\
                {envs.SUBJECT} VARCHAR(100),\
                {envs.ALBUM} VARCHAR(100),\
                {envs.MAKE} VARCHAR(100),\
                {envs.MODEL} VARCHAR(100),\
                {envs.MOUNT} VARCHAR(100),\
                {envs.FOCAL} INT(6),\
                {envs.F_NUMBER} VARCHAR(3),\
                {envs.ISO} INT(5),\
                {envs.LIGHTS} INT(5),\
                {envs.EXPOSURE_TIME} VARCHAR(10),\
                {envs.TOTAL_TIME} VARCHAR(12),\
                {envs.LOCATION} VARCHAR(250),\
                {envs.BORTLE} INT(1),\
                {envs.MOON_PHASE} INT(1),\
                {envs.SOFTWARE} VARCHAR(250),\
                {envs.AUTHOR} VARCHAR(100),\
                {envs.COMMENT} VARCHAR(900),\
                {envs.DATE} VARCHAR(25),\
                {envs.PATH_BRUT} VARCHAR(250) \
                )"

            sql = f"CREATE TABLE {self._name} {data}"
            self._cursor.execute(sql)

    def insert_into(self, data:dict):
        id = data.get(envs.ID)
        if self._row_exists(str(id)):
            return
        # id
        values = (id,)

        # path
        album = data.get(envs.ALBUM)
        path = self.conform_os_file(data.get(envs.PATH), id)
        if not path:
            return
        values += (path,)

        # subject
        values += (data.get(envs.SUBJECT, ""),)

        # album
        values += (album,)

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
        values += (utils.convert_minutes_to_datetime(lights * exposure / 60),)

        # location
        values += (data.get(envs.LOCATION, ""),)
        # bortle
        values += (data.get(envs.BORTLE, 0),)
        # moon
        values += (utils.get_moon_phase(data.get(envs.DATE)),)
        # software
        values += (data.get(envs.SOFTWARE, ""),)
        # author
        values += (data.get(envs.AUTHOR, ""),)
        # comment
        values += (data.get(envs.COMMENT, ""),)
        # date
        values += (data.get(envs.DATE),)
        # brut
        brut = self.conform_os_file(data.get(envs.PATH_BRUT, ""), str(id), version=0)
        if not brut:
            brut = ""
        values += (brut,)
        # current version
        values += (os.path.splitext(os.path.basename(path))[0],)

        sql = f"INSERT INTO {self._name} \
        ({envs.ID},{envs.PATH},{envs.SUBJECT}, \
        {envs.ALBUM},{envs.MAKE},{envs.MODEL}, \
        {envs.MOUNT},{envs.FOCAL},{envs.F_NUMBER}, \
        {envs.ISO},{envs.LIGHTS},{envs.EXPOSURE_TIME}, \
        {envs.TOTAL_TIME},{envs.LOCATION},{envs.BORTLE}, \
        {envs.MOON_PHASE},{envs.SOFTWARE},{envs.AUTHOR}, \
        {envs.COMMENT},{envs.DATE},{envs.PATH_BRUT},{envs.CURRENT_VERSION} \
        ) VALUES (%s,%s,%s,\
            %s,%s,%s,\
                %s,%s,%s,\
                    %s,%s,%s,\
                        %s,%s,%s,\
                            %s,%s,%s,\
                                %s,%s,%s,%s)"

        self._cursor.execute(sql, values)
        self._server.commit()
    
    def get_date(self, id:str):
        result = self.get(envs.DATE, id)
        if result:
            return result[0][0]
        
    def get_path(self, id:str) ->str:
        result = self.get(envs.PATH, id)
        if result:
            return result[0][0]
        
    def get_subject(self, id:str) ->str:
        result = self.get(envs.SUBJECT, id)
        if result:
            return result[0][0]
        
    def get_make(self, id:str) ->str:
        result = self.get(envs.MAKE, id)
        if result:
            return result[0][0]
        
    def get_model(self, id:str) ->str:
        result = self.get(envs.MODEL, id)
        if result:
            return result[0][0]

    def get_mount(self, id:str) ->str:
        result = self.get(envs.MOUNT, id)
        if result:
            return result[0][0]
        
    def get_focal(self, id:str) ->str:
        result = self.get(envs.FOCAL, id)
        if result:
            return result[0][0]

    def get_f_number(self, id:str) ->str:
        result = self.get(envs.F_NUMBER, id)
        if result:
            return result[0][0]
        
    def get_iso(self, id:str) ->str:
        result = self.get(envs.ISO, id)
        if result:
            return result[0][0]
        
    def get_exposure_time(self, id:str) ->str:
        result = self.get(envs.EXPOSURE_TIME, id)
        if result:
            return result[0][0]
        
    def get_lights(self, id:str) ->str:
        result = self.get(envs.LIGHTS, id)
        if result:
            return result[0][0]
        
    def get_total_time(self, id:str) ->str:
        result = self.get(envs.TOTAL_TIME, id)
        if result:
            return result[0][0]
        
    def get_location(self, id:str) ->str:
        result = self.get(envs.LOCATION, id)
        if result:
            return result[0][0]
        
    def get_software(self, id:str) ->str:
        result = self.get(envs.SOFTWARE, id)
        if result:
            return result[0][0]
        
    def get_moon_phase(self, id:str) ->str:
        result = self.get(envs.MOON_PHASE, id)
        if result:
            return result[0][0]
        
    def get_author(self, id:str) ->str:
        result = self.get(envs.AUTHOR, id)
        if result:
            return result[0][0]
        
    def get_comment(self, id:str) ->str:
        result = self.get(envs.COMMENT, id)
        if result:
            return result[0][0]
        
    def get_bortle(self, id:str) ->str:
        result = self.get(envs.BORTLE, id)
        if result:
            return result[0][0]
                        
    def get_current_version(self, id:str):
        result = self.get(envs.CURRENT_VERSION, id)
        if result:
            return result[0][0]
 
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

    def delete_from(self, id:int, path:str):
        # delete from file table
        sql = f"DELETE FROM {self._name} WHERE {envs.ID} = '{str(id)}'"
        self._cursor.execute(sql)
        self._server.commit()

        # delete from version table
        sql = f"DELETE FROM {envs.VERSION_TABLE_NAME} WHERE {envs.VERSION_PARENT_ID} = '{str(id)}'"
        self._cursor.execute(sql)
        self._server.commit()

        # delete from os
        path = Path(path)
        shutil.rmtree(path.parent)
        # os.remove(path.parent / (path.stem + envs.IMAGE_SMALL_SUFFIX + path.suffix))
    
    def _update_total_time(self, id:str):
        # get epxosure total time
        sql = f"SELECT {envs.LIGHTS},{envs.EXPOSURE_TIME} FROM {self._name} WHERE {envs.ID} = '{id}'"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        minutes = float(result[0][0]) * float(result[0][1]) / 60
        total_time = utils.convert_minutes_to_datetime(minutes)

        try:
            sql = f"UPDATE {self._name} SET {envs.TOTAL_TIME} = '{total_time}' WHERE ({envs.ID} = '{id}')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            print(traceback.print_exc())

    def _update_moon_phase(self, date, id:str):
        moon_phase = utils.get_moon_phase(date)
        try:
            sql = f"UPDATE {self._name} SET {envs.MOON_PHASE} = '{moon_phase}' WHERE ({envs.ID} = '{id}')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            print(traceback.print_exc())
    
    def conform_os_file(self, src_path, id, version=1):
        # 0.ext == brut
        # 1.ext == first version
        # 1-small.ext == first version thumbnail

        if os.path.isfile(src_path):
            # create ID directory
            root = os.path.join(envs.ROOT, str(id))
            if not os.path.isdir(root):
                os.makedirs(root)
            
            ext = os.path.splitext(src_path)[-1]
            # create high resolution image path
            dst_full_path = os.path.join(root, f"{str(version)}{ext}")
            while os.path.isfile(dst_full_path):
                version += 1
                dst_full_path = os.path.join(root, f"{str(version)}{ext}")

            shutil.copy(src_path, dst_full_path)

            # reduce image
            image = Image.open(dst_full_path)
            image.thumbnail((300,200))
            dst_small_path = os.path.join(os.path.dirname(dst_full_path),
                                          f"{str(version)}{envs.IMAGE_SMALL_SUFFIX}{ext}")
            image.save(dst_small_path)

            # update
            if self._row_exists(id) and self.get_current_version(id) != version:
                self.update(envs.CURRENT_VERSION, id, version)

            return dst_full_path