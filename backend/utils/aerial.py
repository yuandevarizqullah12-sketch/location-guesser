import aiohttp

async def get_aerial_match(candidate, img_features):
    # OpenAerialMap API (https://api.openaerialmap.org)
    url = f"https://api.openaerialmap.org/v1/imagery?bbox={candidate['lon']-0.01},{candidate['lat']-0.01},{candidate['lon']+0.01},{candidate['lat']+0.01}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if data.get("features"):
                # If aerial imagery exists, assume match (simplified)
                return 20
            else:
                return 0