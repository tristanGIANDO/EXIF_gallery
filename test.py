from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()  # Obtenir les données EXIF de l'image

            if exif_data is not None:
                exif_info = {}
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    exif_info[tag_name] = value
                return exif_info
            else:
                return None
    except Exception as e:
        print(f"Erreur lors de la récupération des données EXIF : {e}")
        return None

# Exemple d'utilisation de la fonction
if __name__ == "__main__":
    image_path = "chemin/vers/votre/image.jpg"
    exif_info = get_exif_data(image_path)
    if exif_info:
        print("Informations EXIF de l'image :")
        for tag, value in exif_info.items():
            print(f"{tag}: {value}")
    else:
        print("Aucune donnée EXIF trouvée pour cette image.")
