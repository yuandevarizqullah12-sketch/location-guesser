import aiohttp
from backend.config import OPEN_ELEVATION_API_KEY

async def get_elevation_score(candidate, img_features):
    # Use Open-Elevation API
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={candidate['lat']},{candidate['lon']}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            elevation = data["results"][0]["elevation"]
            # If image has high edge ratio (mountains) and elevation > 500m
            if img_features["has_edges"] and elevation > 500:
                return 20
            elif not img_features["has_edges"] and elevation < 200:
                return 20
            else:
                return 0