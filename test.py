from PIL import Image
from PIL.ExifTags import TAGS

def convert_bytes_to_str(data):
    if isinstance(data, bytes):
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return "Unable to decode"
    return data

def get_exif_data(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()

            if exif_data is not None:
                exif_info = {}
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    exif_info[tag_name] = convert_bytes_to_str(value)
                return exif_info
            else:
                return None
    except Exception as e:
        print(f"Erreur lors de la récupération des données EXIF : {e}")
        return None

# Exemple d'utilisation de la fonction
if __name__ == "__main__":
    image_path = r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\example2.jpg"
    exif_info = get_exif_data(image_path)
    if exif_info:
        print("Informations EXIF de l'image :")
        for tag, value in exif_info.items():
            print(f"{tag}: {value}")
    else:
        print("Aucune donnée EXIF trouvée pour cette image.")
