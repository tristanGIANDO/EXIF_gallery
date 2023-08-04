import os, shutil, math, decimal, datetime
from skyfield.api import Topos, load
from api import envs

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
   print(parts)
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

if __name__=="__main__":
    # date = datetime.datetime(2030, 2, 1)
    date = "2000/02/29"
    # date = datetime.datetime.now()
    print(get_moon_phase(date))
    # print(get_bortle_level())