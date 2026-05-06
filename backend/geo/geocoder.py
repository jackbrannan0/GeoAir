from backend.utils.redis_client import redis_client
from geopy.geocoders import Nominatim
import asyncio
LOCATION_OVERRIDES = {
    "ukraine": (49.0, 31.0),
    "gaza": (31.5, 34.5),
    "taiwan": (23.5, 121.0),
    "kashmir": (34.0, 76.0),
    "crimea": (45.0, 34.0),
    "kyiv": (50.45, 30.52),
    "moscow": (55.76, 37.62),
    "beijing": (39.90, 116.40),
}

geolocator = Nominatim(user_agent="my_geocoder")

async def geocode_location(locations):
    loop = asyncio.get_running_loop()
    result_locations = []
    try:
        
            for loc in locations:
                 if loc.lower() in LOCATION_OVERRIDES:
                    
                    lat, lon = LOCATION_OVERRIDES[loc.lower()]
                    print(f"Using override for {loc}: {lat}, {lon}")
                    redis_client.set(f"location: {loc}", f"{lat}, {lon}")
                    result = redis_client.get(f"location: {loc}")
                    result_locations.append(result)

                 elif redis_client.exists(f"location: {loc}"):
                    print(f"Cache hit for {loc}")
                    result = redis_client.get(f"location: {loc}")
                    if result:
                        lat, lon = result.split(", ")
                        result_locations.append((lat, lon))
                 else:
                    location = await loop.run_in_executor(None, geolocator.geocode, loc)
                    if not location:
                        print(f"⚠️ Geocoding failed for: {loc}")
                        continue
                    print(location.latitude, location.longitude)
                    redis_client.set(f"location: {loc}", f"{location.latitude}, {location.longitude}")
                    result = redis_client.get(f"location: {loc}")
                    result_locations.append(result)

            return result_locations


    except Exception as e:
        print(f"Error geocoding location: {e}")
        return None
            

    