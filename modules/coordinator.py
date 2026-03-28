import math

class Coordinator:
    def rank(self, candidates, image_labels, clue_text, clue_location, gps, llama_suggestions):
        scored = []
        for cand in candidates:
            score = 0.0

            # 1. Image score: match image labels with place types
            if image_labels:
                common = set(image_labels) & set(cand.get("types", []))
                score += len(common) * 0.2

            # 2. Clue score: if clue text matches name or types
            if clue_text:
                if clue_text.lower() in cand["name"].lower():
                    score += 0.4
                for t in cand.get("types", []):
                    if clue_text.lower() in t.lower():
                        score += 0.2

            # 3. GPS score: if GPS available, distance to candidate
            if gps:
                dist = self._haversine(gps["lat"], gps["lng"], cand["lat"], cand["lng"])
                if dist < 1000:  # within 1 km
                    score += 0.5
                elif dist < 5000:
                    score += 0.2

            # 4. Geocoded clue score: if clue gave coordinates, check distance
            if clue_location:
                dist = self._haversine(clue_location["lat"], clue_location["lng"], cand["lat"], cand["lng"])
                if dist < 1000:
                    score += 0.4
                elif dist < 5000:
                    score += 0.2

            # 5. LLaMA boost (optional)
            if llama_suggestions:
                for sugg in llama_suggestions:
                    if sugg in cand["name"].lower() or any(sugg in t for t in cand.get("types", [])):
                        score += 0.3

            # 6. Cross‑source boost: if candidate appears in both Google and OSM (same place)
            # For simplicity, we just check if source count > 1
            # In real scenario, you'd cross‑reference by location/name

            scored.append((cand, score))

        # Sort by score descending and take top 5
        scored.sort(key=lambda x: x[1], reverse=True)
        top5 = []
        for cand, s in scored[:5]:
            top5.append({
                "name": cand["name"],
                "lat": cand["lat"],
                "lng": cand["lng"],
                "score": round(s, 2),
                "source": cand["source"],
                "types": cand.get("types", [])
            })
        return top5

    @staticmethod
    def _haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R*c