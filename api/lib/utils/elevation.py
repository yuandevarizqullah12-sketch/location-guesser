import aiohttp

async def get_elevation_score(candidate, img_features):
    # Open-Elevation API (gratis, tanpa key)
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={candidate['lat']},{candidate['lon']}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                data = await resp.json()
                elevation = data["results"][0]["elevation"]
                if img_features["has_edges"] and elevation > 500:
                    return 20
                elif not img_features["has_edges"] and elevation < 200:
                    return 20
                else:
                    return 0
        except:
            return 0