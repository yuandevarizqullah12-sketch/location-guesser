import aiohttp
import numpy as np
from PIL import Image
import io

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
                img = img.convert('RGB')
                
                # Konversi ke numpy array untuk analisis
                pixels = np.array(img)
                
                # Hitung green ratio (tanpa OpenCV)
                # Green: nilai green > red AND green > blue
                green_mask = (pixels[:,:,1] > pixels[:,:,0]) & (pixels[:,:,1] > pixels[:,:,2])
                sat_green_ratio = np.mean(green_mask)
                
                diff = abs(sat_green_ratio - img_features["green_ratio"])
                if diff < 0.2:
                    return 20
                else:
                    return 0
        except Exception as e:
            print(f"Esri error: {e}")
            return 0