import traceback, os, shutil
from pathlib import Path
from PIL import Image
from datalens.api import envs, utils
from datalens.api.file import FileTable

class StandardFileTable(FileTable):
    def __init__(self, server) -> None:
        super().__init__(server)
        self._name = envs.STANDARD_FILE_TABLE_NAME

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
                {envs.FOCAL} INT(6),\
                {envs.F_NUMBER} VARCHAR(3),\
                {envs.ISO} INT(5),\
                {envs.EXPOSURE_TIME} VARCHAR(10),\
                {envs.LOCATION} VARCHAR(250),\
                {envs.SOFTWARE} VARCHAR(250),\
                {envs.AUTHOR} VARCHAR(100),\
                {envs.COMMENT} VARCHAR(900),\
                {envs.DATE} VARCHAR(25),\
                {envs.PATH_BRUT} VARCHAR(250)\
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
        # focal
        values += (int(data.get(envs.FOCAL, 0)),)
        # aperture
        values += (data.get(envs.F_NUMBER, 0),)
        # iso
        values += (data.get(envs.ISO, 0),)
        # exposure time
        exposure = data.get(envs.EXPOSURE_TIME, 0)
        values += (exposure,)
        # location
        values += (data.get(envs.LOCATION, ""),)
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
    
        sql = f"INSERT INTO {self._name} \
        ({envs.ID},{envs.PATH},{envs.SUBJECT}, \
        {envs.ALBUM},{envs.MAKE},{envs.MODEL}, \
        {envs.FOCAL},{envs.F_NUMBER}, \
        {envs.ISO},{envs.EXPOSURE_TIME}, \
        {envs.LOCATION},\
        {envs.SOFTWARE},{envs.AUTHOR}, \
        {envs.COMMENT},{envs.DATE},{envs.PATH_BRUT} \
        ) VALUES (%s,%s,%s,\
            %s,%s,%s,\
                %s,%s,%s,\
                    %s,%s,%s,\
                        %s,%s,%s,\
                            %s)"

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
        
    def get_location(self, id:str) ->str:
        result = self.get(envs.LOCATION, id)
        if result:
            return result[0][0]
        
    def get_software(self, id:str) ->str:
        result = self.get(envs.SOFTWARE, id)
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