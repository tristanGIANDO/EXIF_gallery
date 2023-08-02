import os, shutil, math, decimal, datetime
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
       
def get_moon_phase(date): 
   dec = decimal.Decimal
   diff = date - datetime.datetime(2001, 1, 1)
   days = dec(diff.days) + (dec(diff.seconds) / dec(86400))
   lunations = dec("0.20439731") + (days * dec("0.03386319269"))

   pos = lunations % dec(1)
   index = (pos * dec(8)) + dec("0.5")
   index = math.floor(index)
   return {
      0: "New Moon", 
      1: "Waxing Crescent", 
      2: "First Quarter", 
      3: "Waxing Gibbous", 
      4: "Full Moon", 
      5: "Waning Gibbous", 
      6: "Last Quarter", 
      7: "Waning Crescent"
   }[int(index) & 7]

if __name__=="__main__":
   date = datetime.datetime(2030, 2, 1)
   # date = datetime.datetime.now()
   print(get_moon_phase(date))
