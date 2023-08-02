import os, shutil
from api_sql import envs

def copy_file(path:str,id:str) ->str:
       if os.path.isfile(path):
        if not os.path.isdir(envs.ROOT):
              os.mkdir(envs.ROOT)
        new_path = os.path.join(envs.ROOT, f"{id}{os.path.splitext(path)[-1]}")
        shutil.copy(path, new_path)

        return new_path
       
def convert_minutes_to_datetime(time):
      hours, seconds = divmod(time * 60, 3600)
      minutes, seconds = divmod(seconds, 60)
      return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"