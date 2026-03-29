from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io

async def extract_metadata(image_bytes):
    img = Image.open(io.BytesIO(image_bytes))
    exif = img._getexif()
    if not exif:
        return {"gps": None, "bonus": 0}

    gps = {}
    for tag, value in exif.items():
        tag_name = TAGS.get(tag, tag)
        if tag_name == "GPSInfo":
            for gps_tag in value:
                gps_name = GPSTAGS.get(gps_tag, gps_tag)
                gps[gps_name] = value[gps_tag]

    if gps and "GPSLatitude" in gps and "GPSLongitude" in gps:
        lat = convert_to_degrees(gps["GPSLatitude"])
        lon = convert_to_degrees(gps["GPSLongitude"])
        return {"gps": (lat, lon), "bonus": 10}
    else:
        return {"gps": None, "bonus": 0}

def convert_to_degrees(value):
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)