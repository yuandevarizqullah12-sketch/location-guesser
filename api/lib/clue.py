from geopy.geocoders import Nominatim
import asyncio

geolocator = Nominatim(user_agent="location_guesser")

async def process_clue(clue_text):
    if not clue_text:
        return {"location": None, "bonus": 0}

    try:
        # Geocode dengan timeout
        location = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None, geolocator.geocode, clue_text
            ),
            timeout=5.0
        )
        if location:
            return {
                "location": {
                    "lat": location.latitude,
                    "lon": location.longitude,
                    "address": location.address
                },
                "bonus": 10
            }
        else:
            return {"location": None, "bonus": 0}
    except:
        return {"location": None, "bonus": 0}