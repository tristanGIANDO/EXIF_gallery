import os, shutil
from smoke.api import envs, utils
from PIL import Image

class VersionTable(object):
    def __init__(self, server) -> None:
        self._server = server
        self._cursor = server.cursor(buffered=True)
        self._name = envs.VERSION_TABLE_NAME

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
                {envs.ID} INT AUTO_INCREMENT PRIMARY KEY,\
                {envs.VERSION_PATH} VARCHAR(250),\
                {envs.VERSION_PARENT_ID} VARCHAR(250)\
                )"

            sql = f"CREATE TABLE {self._name} {data}"
            self._cursor.execute(sql)

    def delete(self):
        sql = f"DROP TABLE {self._name}"
        self._cursor.execute(sql)

    def insert_into(self, version_path, parent_id):
        # version path
        version_path = self.conform_os_file(version_path, parent_id, version=2)
        if not version_path:
            return
        values = (version_path,)

        # parent id
        values += (parent_id,)

        sql = f"INSERT INTO {self._name} \
        ({envs.VERSION_PATH},{envs.VERSION_PARENT_ID}) VALUES (%s,%s)"

        self._cursor.execute(sql, values)
        self._server.commit()

    def select_rows(self):
        self._cursor.execute(f"SELECT * FROM {self._name}")
        return self._cursor.fetchall()
    
    def select_from_column(self, column:str, value:str):
        sql = f"SELECT * FROM {self._name} WHERE {column} ='{value}'"
        self._cursor.execute(sql)
        return self._cursor.fetchall()
    
    def get(self, column:str, id:str):
        sql = f"SELECT {column} FROM {self._name} WHERE {envs.ID} ='{id}'"
        self._cursor.execute(sql)
        return self._cursor.fetchall()
    
    def update(self, column:str, id:str, new_value:str):
        # global update
        try:
            sql = f"UPDATE {self._name} SET {column} = '{new_value}' WHERE ({envs.ID} = '{str(id)}')"
            self._cursor.execute(sql)
            self._server.commit()
        except:
            pass

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
        
    def get_versions(self, id):
        return self.select_from_column(envs.VERSION_PARENT_ID, id)

        # path = self.get_path(id)
        # basename = os.path.basename(path)

        # versions = []
        # for i in range(self.get_current_version(id)):
        #     version = os.path.join(path, basename.replace(str(i), str(i)))

    def get_versions_paths(self, id):
        versions = self.select_from_column(envs.VERSION_PARENT_ID, id)
        if versions:
            return [v[1] for v in versions]
        else:
            return []