import aiohttp
import random
import asyncio

async def query_osm_candidates(img_features, clue_info, metadata):
    # Simplified: use Overpass to fetch features based on environment
    if clue_info["location"]:
        lat, lon = clue_info["location"]["lat"], clue_info["location"]["lon"]
        bbox = f"{lat-0.5},{lon-0.5},{lat+0.5},{lon+0.5}"
    else:
        bbox = "-90,-180,90,180"  # world

    # Choose query based on environment
    if img_features["environment"] == "natural":
        query = """
        [out:json];
        (
          node["natural"="wood"]({bbox});
          node["natural"="water"]({bbox});
          way["natural"="wood"]({bbox});
          way["natural"="water"]({bbox});
        );
        out center 10;
        """.format(bbox=bbox)
    else:
        query = """
        [out:json];
        (
          node["highway"]({bbox});
          node["building"]({bbox});
          way["highway"]({bbox});
          way["building"]({bbox});
        );
        out center 10;
        """.format(bbox=bbox)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://overpass-api.de/api/interpreter",
            data={"data": query}
        ) as resp:
            data = await resp.json()
            candidates = []
            for element in data.get("elements", []):
                lat = element.get("lat") or element.get("center", {}).get("lat")
                lon = element.get("lon") or element.get("center", {}).get("lon")
                if lat and lon:
                    candidates.append({
                        "lat": lat,
                        "lon": lon,
                        "name": element.get("tags", {}).get("name", "Unnamed"),
                        "type": element.get("type"),
                        "tags": element.get("tags", {})
                    })
            return candidates[:10]

async def score_osm_match(candidate, img_features):
    # Simple rule: natural areas get points if image has high green ratio
    if img_features["environment"] == "natural":
        if "natural" in candidate["tags"]:
            return 20
        elif "landuse" in candidate["tags"] and candidate["tags"]["landuse"] in ["forest", "grass"]:
            return 20
        else:
            return 0
    else:
        if "highway" in candidate["tags"] and img_features["has_edges"]:
            return 20
        elif "building" in candidate["tags"] and img_features["edge_ratio"] > 0.05:
            return 20
        else:
            return 0