from pathlib import Path

path = Path(__file__)
icons_root = path.parent / "icons"

ICONS = {
    "add_file" : f"{icons_root}/add_image.png",
    "remove_file" : f"{icons_root}/remove_image.png",
    "reload" : f"{icons_root}/reload.png",
    0 : f"{icons_root}/0.png",
    1 : f"{icons_root}/1.png",
    2 : f"{icons_root}/2.png",
    3 : f"{icons_root}/3.png",
    4 : f"{icons_root}/4.png",
    5 : f"{icons_root}/5.png",
    6 : f"{icons_root}/6.png",
    7 : f"{icons_root}/7.png",
    
}

# global infos
G_ID = "ID"
G_PATH = "Path"
G_IMAGE = "Image"
G_SUBJECT = "Subject"
G_DESC = "Description"
G_CAMERA = "Camera"
G_FOCAL = "Focal Length (mm)"
G_APERTURE = "Aperture"
G_ISO = "ISO"
G_EXPOSURE_TIME = "Exposure Time (seconds)"
G_LOCATION = "Location"
G_PROCESS = "Processed with"
G_AUTHOR = "Author"
G_COMMENT = "Comment"
G_DATE = "Date"

# astro infos
A_MOUNT = "Mount"
A_LIGHTS = "NB Lights"
A_BORTLE = "Sky Darkness"
A_MOON = "Moon Phase"
A_TIME = "Total Time"

MOON_PHASES = {
      0: "New Moon", 
      1: "Waxing Crescent", 
      2: "First Quarter", 
      3: "Waxing Gibbous", 
      4: "Full Moon", 
      5: "Waning Gibbous", 
      6: "Last Quarter", 
      7: "Waning Crescent"
   }