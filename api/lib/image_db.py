import asyncio
from .utils.mapillary import get_mapillary_match
from .utils.aerial import get_aerial_match

async def validate_with_images(candidates, img_features):
    async def enrich(candidate):
        try:
            map_score = await asyncio.wait_for(
                get_mapillary_match(candidate, img_features), timeout=3.0
            )
            aerial_score = await asyncio.wait_for(
                get_aerial_match(candidate, img_features), timeout=3.0
            )
        except asyncio.TimeoutError:
            map_score = aerial_score = 0
        candidate["scores"]["mapillary"] = map_score
        candidate["scores"]["aerial"] = aerial_score
        return candidate

    enriched = await asyncio.gather(*[enrich(c) for c in candidates])
    return enriched