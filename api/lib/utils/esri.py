import aiohttp
import numpy as np
from PIL import Image
import io
import cv2

async def get_satellite_match_score(candidate, img_features):
    # Ambil tile dari Esri World Imagery
    url = "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export"
    params = {
        "bbox": f"{candidate['lon']-0.01},{candidate['lat']-0.01},{candidate['lon']+0.01},{candidate['lat']+0.01}",
        "bboxSR": 4326,
        "size": "256,256",
        "imageSR": 4326,
        "format": "png",
        "f": "image"
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=3)) as resp:
                img_bytes = await resp.read()
                img = Image.open(io.BytesIO(img_bytes))
                img = np.array(img.convert('RGB'))
                # Hitung green ratio
                hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
                green_mask = cv2.inRange(hsv, (40, 50, 20), (80, 255, 255))
                sat_green_ratio = np.sum(green_mask > 0) / (img.shape[0] * img.shape[1])
                diff = abs(sat_green_ratio - img_features["green_ratio"])
                if diff < 0.2:
                    return 20
                else:
                    return 0
        except:
            return 0