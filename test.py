from PIL import Image

def update_exif_data(image_path, new_author_name):
    try:
        with Image.open(image_path) as img:
            # Obtenir les métadonnées EXIF
            exif_data = img.info.get("exif")

            # Vérifier si les métadonnées EXIF existent
            if exif_data:
                # Convertir les métadonnées en un dictionnaire
                exif_dict = dict(exif_data)

                # Définir le nouveau nom de l'auteur (ou tout autre tag EXIF que vous souhaitez modifier)
                new_author_tag = 0x013B  # Exemple de tag pour le nom de l'auteur (0x013B)
                exif_dict[new_author_tag] = new_author_name

                # Convertir le dictionnaire des métadonnées en format bytes
                exif_bytes = ExifIFD.format(exif_dict)

                # Mettre à jour les métadonnées EXIF de l'image
                img.save(image_path, exif=exif_bytes)

                print("Métadonnées EXIF mises à jour avec succès.")
            else:
                print("Aucune métadonnée EXIF trouvée dans l'image.")

    except Exception as e:
        print(f"Erreur lors de la mise à jour des métadonnées EXIF : {e}")

# Exemple d'utilisation
if __name__ == "__main__":
    image_path = r"C:\Users\giand\OneDrive\Documents\packages\PHOTO_GALLERY\dev\example2.jpg"
    new_author_name = "Nouvel auteur"  # Nouveau nom de l'auteur que vous souhaitez définir

    update_exif_data(image_path, new_author_name)
