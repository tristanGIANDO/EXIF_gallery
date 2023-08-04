import os, shutil, math, decimal, datetime
# from skyfield.api import Topos, load
from gallery.api import envs

from PIL import Image
from PIL.ExifTags import TAGS

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
       
def get_moon_phase(date):
   parts = date.split(",")
   date = datetime.datetime(int(parts[0]), int(parts[1]), int(parts[2]))
   dec = decimal.Decimal
   diff = date - datetime.datetime(2001, 1, 1)
   days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
   lunations = dec("0.20439731") + (days * dec("0.03386319269"))

   pos = lunations % dec(1)
   index = (pos * dec(8)) + dec("0.5")
   index = math.floor(index)

   return int(index) & 7

def get_bortle_level():
    latitude = 43.599916923299425
    longitude = 3.8750995364824687

    ts = load.timescale()
    planete = load('de421.bsp')
    lieu = Topos(latitude_degrees=latitude, longitude_degrees=longitude)

    t = ts.now()
    astres = planete['hip']
    astres_at_lieu = astres.at(t).observe(lieu)
    apparent = astres_at_lieu.apparent()
    magnitude_limite = apparent.mag

    if magnitude_limite <= 2.0:
            return 1
    elif magnitude_limite <= 4.0:
        return 2
    elif magnitude_limite <= 4.5:
        return 3
    elif magnitude_limite <= 5.0:
        return 4
    elif magnitude_limite <= 5.5:
        return 5
    elif magnitude_limite <= 6.0:
        return 6
    elif magnitude_limite <= 7.0:
        return 7
    elif magnitude_limite <= 8.0:
        return 8
    elif magnitude_limite <= 9.0:
        return 9
    else:
        return 10

def get_exifs(path):
    data = {}
    # add custom data
    data[envs.ID] = os.stat(path).st_ino
    data[envs.SUBJECT] = os.path.splitext(os.path.basename(path))[0]
    data[envs.PATH] = path
    
    # add exifs
    with Image.open(path) as img:
        exif_data = img._getexif()

        if exif_data:
            for tag, value in exif_data.items():
                # tag_name = TAGS.get(tag, tag)
                # decode bytes
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8')
                    except:
                        continue
                db_name = envs.EXIF_TO_DATABASE_MAPPING.get(tag,"")
                if db_name:
                    data[db_name] = str(value)

    return data

if __name__=="__main__":
    import json
    print(json.dumps(get_exifs(r"\\192.168.1.51\Roaming_Profile\trigi\Desktop\work environment\a.jpg"), indent=4))