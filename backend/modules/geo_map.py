from utils.osm import query_osm_candidates, score_osm_match
from utils.elevation import get_elevation_score
from utils.esri import get_satellite_match_score
import asyncio

async def get_candidates(img_features, clue_info, metadata):
    # Get candidate coordinates from OSM based on environment and clue
    candidates = await query_osm_candidates(img_features, clue_info, metadata)

    # For each candidate, compute map layer scores
    async def enrich(candidate):
        # OSM match
        osm_score = await score_osm_match(candidate, img_features)

        # Topo match (elevation)
        topo_score = await get_elevation_score(candidate, img_features)

        # Satellite match
        sat_score = await get_satellite_match_score(candidate, img_features)

        candidate["scores"] = {
            "osm": osm_score,
            "topo": topo_score,
            "satellite": sat_score
        }
        return candidate

    enriched = await asyncio.gather(*[enrich(c) for c in candidates])
    return enriched