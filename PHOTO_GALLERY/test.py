from database.database import Database
from image.exif_file import ExifFile

database_path = r"C:\Users\giand\.database.json"
file_path = r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\example2.jpg"
# file_path = r"C:\Users\giand\OneDrive\Images\@PORTFOLIO\230219_m31_04.jpg"

server = Database(database_path)
# a_files = server.get_files()
# # file = a_files[0]
# # print (file.get_key())

# exif_file = ExifFile(file_path)
# file = server.create_file(exif_file.get_key(),
#                           str(exif_file.get_image()),
#                           name=exif_file.get_name(),
#                           path=exif_file.get_path()
#                           )
# server.save()


# b_files = server.get_files()
server.remove_file(1688849860292696)
# print(server)
# print(a_files)
# print(exif_file)
# print(file)
# print(b_files)

# def image_to_bytes(image_path):
#     with open(image_path, 'rb') as image_file:
#         bytes_data = image_file.read()
#     return bytes_data

# donnees_en_bytes = image_to_bytes(file_path)

# print(donnees_en_bytes)