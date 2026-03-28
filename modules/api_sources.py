import httpx
import os
from urllib.parse import quote

async def search_google_places(query, gps_coords=None):
    """Search Google Places using text search or nearby search."""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        return []
    async with httpx.AsyncClient() as client:
        if query and isinstance(query, str):
            # Text search
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            params = {
                "query": query,
                "key": api_key
            }
        elif gps_coords:
            # Nearby search
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                "location": f"{gps_coords['lat']},{gps_coords['lng']}",
                "radius": 5000,
                "key": api_key
            }
        else:
            return []
        resp = await client.get(url, params=params)
        data = resp.json()
        results = []
        for place in data.get("results", []):
            results.append({
                "name": place["name"],
                "lat": place["geometry"]["location"]["lat"],
                "lng": place["geometry"]["location"]["lng"],
                "place_id": place["place_id"],
                "types": place.get("types", []),
                "source": "google"
            })
        return results

async def search_osm(query):
    """Search OpenStreetMap using Nominatim."""
    async with httpx.AsyncClient() as client:
        if isinstance(query, str):
            params = {"q": query, "format": "json", "limit": 5}
        else:
            # If query is a coordinate dict, reverse geocode
            params = {"lat": query["lat"], "lon": query["lng"], "format": "json"}
        resp = await client.get("https://nominatim.openstreetmap.org/search", params=params)
        data = resp.json()
        results = []
        for item in data:
            results.append({
                "name": item.get("display_name", ""),
                "lat": float(item["lat"]),
                "lng": float(item["lon"]),
                "place_id": item.get("osm_id"),
                "types": [item.get("type", "")],
                "source": "osm"
            })
        return results

async def search_wikidata(entity):
    """Placeholder: query Wikidata for location details."""
    # In a real implementation you'd use SPARQL
    return []