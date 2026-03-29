import os
import aiohttp

MAPILLARY_API_KEY = os.getenv("MAPILLARY_API_KEY")

async def get_mapillary_match(candidate, img_features):
    if not MAPILLARY_API_KEY:
        return 0
    query = """
    {
      search_photos(
        bbox: { minLon: %f, minLat: %f, maxLon: %f, maxLat: %f },
        limit: 10
      ) {
        id
        geometry { coordinates }
      }
    }
    """ % (candidate["lon"]-0.01, candidate["lat"]-0.01, candidate["lon"]+0.01, candidate["lat"]+0.01)

    headers = {"Authorization": f"OAuth {MAPILLARY_API_KEY}"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "https://graph.mapillary.com",
                json={"query": query},
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=3)
            ) as resp:
                data = await resp.json()
                if data.get("data", {}).get("search_photos"):
                    return 20
                else:
                    return 0
        except:
            return 0