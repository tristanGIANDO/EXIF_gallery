from database.database import Database

database_path = r"C:\Users\giand\.database.json"
file_path = r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\example2.jpg"

server = Database(database_path)
files = server.get_files()

print(server)
print(files)