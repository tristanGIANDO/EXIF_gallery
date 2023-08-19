import os, shutil, math, decimal, datetime
# from skyfield.api import Topos, load
from datalens.api import envs
import ast
from pathlib import Path
from PIL import Image
# from PIL.ExifTags import TAGS

def copy_file(path:str,id:str) ->str:
    """copy file to dir

    Args:
        path (str): _description_
        id (str): _description_

    Returns:
        str: _description_
    """
    if os.path.isfile(path):
        if not os.path.isdir(envs.ROOT):
            os.mkdir(envs.ROOT)
        new_path = os.path.join(envs.ROOT, f"{id}{os.path.splitext(path)[-1]}")
        shutil.copy(path, new_path)

        return new_path
    else:
        return ""
       
def convert_minutes_to_datetime(time):
    """convert

    Args:
        time (_type_): _description_

    Returns:
        _type_: _description_
    """
    hours, seconds = divmod(time * 60, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"
       
def get_moon_phase(date):
   parts = date.split(",")
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

def get_exifs(path):
    if not os.path.isfile(path):
        # raise FileNotFoundError(f"{path} is not a file.")
        return
    
    data = {}
    # add custom data
    data[envs.ID] = os.stat(path).st_ino
    data[envs.SUBJECT] = os.path.splitext(os.path.basename(path))[0]
    data[envs.PATH] = path
    
    # add exifs
    with Image.open(path) as img:
        exif_data = img._getexif()

        if exif_data:
            for tag, value in exif_data.items():
                # tag_name = TAGS.get(tag, tag)
                # decode bytes
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8')
                    except:
                        continue
                db_name = envs.EXIF_TO_DATABASE_MAPPING.get(tag,"")
                if db_name:
                    data[db_name] = str(value)

    return data

def resize_image(path:str, w:int, h:int):
    path = Path(path)
    image = Image.open(path)
    image.thumbnail((w,h))
    result = path.parent / (path.stem + envs.IMAGE_SMALL_SUFFIX + path.suffix)
    image.save(result)
    
    return result

def create_website(self, paths):
    text = ""

def ouvrir_et_editer_fichier_html(nom_fichier):
    try:
        # Ouvrir le fichier en mode lecture
        with open(nom_fichier, 'r') as fichier:
            lignes = fichier.readlines()

        # Filtrer les lignes à conserver (supprimer celles qui commencent par </div> et <div>)
        # lignes_modifiees = [ligne for ligne in lignes if not ligne.strip().startswith('</div') and not ligne.strip().startswith('<div') and not ligne.strip().startswith('<img')]
        lignes += ["""
blabla
    blibli
        """]
        # Ouvrir le fichier en mode écriture pour écrire les lignes modifiées
        with open(nom_fichier, 'w') as fichier_modifie:
            fichier_modifie.writelines(lignes)

        print(f"Les lignes contenant </div> et <div> ont été supprimées du fichier {nom_fichier}.")
    except FileNotFoundError:
        print(f"Le fichier {nom_fichier} n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

def doc_to_web(file_path, delivery_path):
    # Contenu HTML à écrire dans le fichier
    html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YOUR NAME</title>
    <style>
        /* Ajoutez votre CSS ici pour le style */
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #f2f2f2;
            padding: 10px;
            text-align: center;
        }
        nav {
            background-color: #333;
            color: #fff;
            padding: 10px;
            text-align: center;
        }
        nav a {
            color: #fff;
            text-decoration: none;
            margin: 0 10px;
        }
        section {
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        footer {
            background-color: #f2f2f2;
            padding: 10px;
            text-align: center;
        }
        .gallery-container {
            display: flex;
            flex-wrap: wrap;
        }
        .gallery-item {
            width: 33.33%; /* 3 colonnes pour une grille */
            padding: 5px;
            box-sizing: border-box;
        }

        .gallery-item img {
            width: 100%;
            height: auto;
            display: block;
        }
    </style>
</head>
<body>
    <header>
        <h1>your tool</h1>
    </header>
    <nav>
        <a href="#">Home</a>
        <a href="#">About me</a>
        <a href="#">Contact</a>
    </nav>
"""
    with open(file_path, 'r') as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            html_content += (f"<h2>DEF {node.name}<h2>")
            html_content += (f"<p>{node.name.__doc__}<p>")

    html_content += """
<footer>
        <p>All rights reserved &copy; 2023 your tool</p>
    </footer>
</body>
</html>
"""

    # Chemin du fichier HTML à créer
    fichier_html = os.path.join(delivery_path, "mon_fichier.html")

    # Écrire le contenu HTML dans le fichier
    with open(fichier_html, "w") as f:
        f.write(html_content)

    print(f"Le fichier '{fichier_html}' a été créé avec succès.")

# 

# def get_function_names(file_path):
#     with open(file_path, 'r') as file:
#         source_code = file.read()

#     tree = ast.parse(source_code)
#     function_names = []

#     for node in ast.walk(tree):
#         if isinstance(node, ast.FunctionDef):
#             function_names.append(node.name)
#             print(f"<p>{node.name.__doc__}<p>")

#     return function_names

# file_path = __file__  # Remplace avec le chemin vers ton fichier Python
# function_names = get_function_names(file_path)
# print("Noms des fonctions dans le fichier : ", function_names)

if __name__=="__main__":
    # print(resize_image(r"\\192.168.1.51\Roaming_Profile\trigi\Desktop\work environment\a.jpg", 150, 100))
    # print(get_exifs(r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\IMG_5555.JPG"))

    doc_to_web(__file__, r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\datalens")

#     with open(__file__, 'r') as fichier:
#         lignes = fichier.readlines()
#         defs = [ligne for ligne in lignes if ligne.strip().startswith('def')]

#         print(defs)