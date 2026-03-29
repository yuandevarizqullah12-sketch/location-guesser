def rank_locations(candidates, img_features, clue_info, metadata):
    for candidate in candidates:
        scores = candidate["scores"]
        total = (
            scores.get("osm", 0) +
            scores.get("topo", 0) +
            scores.get("satellite", 0) +
            scores.get("mapillary", 0) +
            scores.get("aerial", 0)
        )
        # Bonus: if clue matches location (simplified)
        if clue_info["location"] and is_near(candidate, clue_info["location"]):
            total += clue_info["bonus"]
        # Bonus: if GPS matches candidate (simplified)
        if metadata["gps"] and is_near(candidate, metadata["gps"]):
            total += metadata["bonus"]

        candidate["confidence"] = round((total / 110) * 100, 2)
        candidate["total_score"] = total

    candidates.sort(key=lambda x: x["total_score"], reverse=True)
    return candidates[:5]

def is_near(candidate, point, threshold_km=10):
    # Simplified: approximate haversine distance
    from math import radians, sin, cos, sqrt, atan2
    lat1, lon1 = candidate["lat"], candidate["lon"]
    lat2, lon2 = point
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance < threshold_km