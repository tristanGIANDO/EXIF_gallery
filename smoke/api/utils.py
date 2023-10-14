import os, math, decimal, datetime
from smoke.api import envs
from pathlib import Path
from PIL import Image
import ephem
       
def convert_minutes_to_datetime(time):
    """convert

    Args:
        time (_type_): _description_

    Returns:
        _type_: _description_
    """
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

def get_bortle_level(latitude, longitude):
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)

    sun = ephem.Sun()
    sun.compute(observer)
    magnitude_limite = sun.mag

    bortle_score = determine_bortle_score(magnitude_limite)
    print(f"Le score Bortle de ce lieu est : {bortle_score}")

def determine_bortle_score(magnitude_limite):
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
    if not os.path.isfile(path):
        # raise FileNotFoundError(f"{path} is not a file.")
        return
    
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

def resize_image(path:str, w:int, h:int):
    path = Path(path)
    image = Image.open(path)
    image.thumbnail((w,h))
    result = path.parent / (path.stem + envs.IMAGE_SMALL_SUFFIX + path.suffix)
    image.save(result)
    
    return result

if __name__=="__main__":
    get_bortle_level()