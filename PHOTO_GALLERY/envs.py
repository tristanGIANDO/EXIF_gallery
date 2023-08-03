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

G_ID = "ID"
G_PATH = "Path"
G_IMAGE = "Image"
G_SUBJECT = "Subject"
G_DESC = "Description"
G_CAMERA = "Camera"
G_FOCAL = "Focal Length (mm)"
A_MOUNT = "Mount"
G_APERTURE = "Aperture"
G_ISO = "ISO"
A_LIGHTS = "NB Lights"
G_EXPOSURE_TIME = "Exposure Time (seconds)"
A_TIME = "Total Time"
G_LOCATION = "Location"
A_BORTLE = "Sky Darkness"
A_MOON = "Moon Phase"
G_PROCESS = "Processed with"
G_AUTHOR = "Author"
G_COMMENT = "Comment"
G_DATE = "Date"

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