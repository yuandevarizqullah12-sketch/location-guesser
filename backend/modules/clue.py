from geopy.geocoders import Nominatim
import asyncio

geolocator = Nominatim(user_agent="location_guesser")

async def process_clue(clue_text):
    if not clue_text:
        return {"location": None, "bonus": 0}

    try:
        location = geolocator.geocode(clue_text)
        if location:
            return {
                "location": {
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "address": location.address
                },
                "bonus": 10   # bonus for clue match later
            }
        else:
            return {"location": None, "bonus": 0}
    except:
        return {"location": None, "bonus": 0}