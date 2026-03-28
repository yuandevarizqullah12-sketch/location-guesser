import httpx
import os

async def geocode_clue(clue: str):
    """Convert clue text to coordinates using Google Geocoding."""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return None
    async with httpx.AsyncClient() as client:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": clue, "key": api_key}
        resp = await client.get(url, params=params)
        data = resp.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return {"lat": location["lat"], "lng": location["lng"]}
    return None