import asyncio
from .utils.osm import query_osm_candidates, score_osm_match
from .utils.elevation import get_elevation_score
from .utils.esri import get_satellite_match_score

async def get_candidates(img_features, clue_info, metadata):
    # Ambil kandidat dari OSM berdasarkan environment & clue
    candidates = await query_osm_candidates(img_features, clue_info, metadata)
    if not candidates:
        return []

    # Enrich dengan skor dari masing-masing layer
    async def enrich(candidate):
        try:
            # OSM
            osm_score = await asyncio.wait_for(
                score_osm_match(candidate, img_features), timeout=3.0
            )
            # Topo (elevation)
            topo_score = await asyncio.wait_for(
                get_elevation_score(candidate, img_features), timeout=3.0
            )
            # Satellite
            sat_score = await asyncio.wait_for(
                get_satellite_match_score(candidate, img_features), timeout=3.0
            )
            candidate["scores"] = {
                "osm": osm_score,
                "topo": topo_score,
                "satellite": sat_score
            }
        except asyncio.TimeoutError:
            candidate["scores"] = {"osm": 0, "topo": 0, "satellite": 0}
        return candidate

    # Batasi jumlah kandidat untuk kecepatan
    candidates = candidates[:5]
    enriched = await asyncio.gather(*[enrich(c) for c in candidates])
    return enriched