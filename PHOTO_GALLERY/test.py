from database.database import Database
from image.exif_file import ExifFile

database_path = r"C:\Users\giand\.database.json"
# file_path = r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\example2.jpg"
file_path = r"C:\Users\giand\OneDrive\Images\@PORTFOLIO\230219_m31_04.jpg"

server = Database(database_path)
a_files = server.get_files()

exif_file = ExifFile(file_path)
file = server.create_file(exif_file.get_key(), name=exif_file.get_name())
server.save()

b_files = server.get_files()

print(server)
print(a_files)
print(exif_file)
print(file)
print(b_files)