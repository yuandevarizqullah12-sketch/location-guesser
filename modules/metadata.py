import piexif
from io import BytesIO

def convert_to_degrees(value):
    """Convert GPS coordinates from EXIF format to decimal degrees."""
    d, m, s = value
    return d + (m / 60.0) + (s / 3600.0)

def extract_gps(image_bytes: bytes):
    try:
        exif_dict = piexif.load(image_bytes)
        gps = exif_dict.get('GPS', {})
        if not gps:
            return None
        lat = convert_to_degrees(gps[piexif.GPSIFD.GPSLatitude])
        lon = convert_to_degrees(gps[piexif.GPSIFD.GPSLongitude])
        lat_ref = gps.get(piexif.GPSIFD.GPSLatitudeRef, b'N').decode()
        lon_ref = gps.get(piexif.GPSIFD.GPSLongitudeRef, b'E').decode()
        if lat_ref == 'S':
            lat = -lat
        if lon_ref == 'W':
            lon = -lon
        return {"lat": lat, "lng": lon}
    except:
        return None