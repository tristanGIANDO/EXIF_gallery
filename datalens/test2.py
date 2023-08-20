files = [
    {"id":0, "album" : "astro"},
    {"id":1, "album" : "astro"},
    {"id":2, "album" : "paysage"},
    {"id":3, "album" : "astro_manon"},
    {"id":4, "album" : "astro"},
    {"id":5, "album" : "paysage"},
]

albums = {}
for file in files:
    album = file.get("album")
    if not album in albums:
        albums[album] = [file.get("id")]
    else:
        albums[album].append(file.get("id"))

print(albums)