from api_sql.db import Database
from api.exif_file import ExifFile

db = Database()
file = ExifFile(r"C:\Users\giand\OneDrive\Images\@PORTFOLIO\230624 ecu.jpg")

data = {"id" : file.get_id(),
        "subject" : file.get_name(),
        "path" : file.get_path(),
        "date" : "2023/03/29"}
db.add(data)
