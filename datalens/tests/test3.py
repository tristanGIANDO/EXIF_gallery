from geopy.geocoders import Nominatim

def get_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location:
        return location.address
    else:
        return "Lieu inconnu"

latitude = 48.8566  # Exemple de latitude (Paris, France)
longitude = 2.3522  # Exemple de longitude (Paris, France)

location_name = get_location_name(latitude, longitude)
print("Nom du lieu:", location_name)
