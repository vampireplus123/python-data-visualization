import googlemaps as ggms

API_Key = "AIzaSyAk80WplCgEu0vBuwcPyelokUNuOYkylW8"
gmaps = ggms.Client(key=API_Key)

address = "1600 Amphitheatre Parkway, Mountain View, CA"
geocode_result = gmaps.geocode(address)
if geocode_result:
    location = geocode_result[0]['geometry']['location']
    print(f"Latitude: {location['lat']}, Longitude: {location['lng']}")