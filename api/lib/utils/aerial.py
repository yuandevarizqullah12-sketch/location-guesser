import aiohttp

async def get_aerial_match(candidate, img_features):
    url = f"https://api.openaerialmap.org/v1/imagery?bbox={candidate['lon']-0.01},{candidate['lat']-0.01},{candidate['lon']+0.01},{candidate['lat']+0.01}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                data = await resp.json()
                if data.get("features"):
                    return 20
                else:
                    return 0
        except:
            return 0