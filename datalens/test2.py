files = [
    {"id":0, "album" : "astro"},
    {"id":1, "album" : "astro"},
    {"id":2, "album" : "paysage"},
    {"id":3, "album" : "astro_manon"},
    {"id":4, "album" : "astro"},
    {"id":5, "album" : "paysage"},
]

current_album = "astro"
album_files = []
for file in files:
    album = file.get("album")
    if album == current_album:
        album_files.append(file)

print(album_files)