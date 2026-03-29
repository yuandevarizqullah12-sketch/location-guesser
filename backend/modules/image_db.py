from utils.mapillary import get_mapillary_match
from utils.aerial import get_aerial_match
import asyncio

async def validate_with_images(candidates, img_features):
    async def enrich(candidate):
        map_score = await get_mapillary_match(candidate, img_features)
        aerial_score = await get_aerial_match(candidate, img_features)
        candidate["scores"]["mapillary"] = map_score
        candidate["scores"]["aerial"] = aerial_score
        return candidate

    enriched = await asyncio.gather(*[enrich(c) for c in candidates])
    return enriched