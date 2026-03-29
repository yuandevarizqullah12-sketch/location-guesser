import os
from dotenv import load_dotenv

load_dotenv()

MAPILLARY_API_KEY = os.getenv("MAPILLARY_API_KEY")
OPEN_ELEVATION_API_KEY = os.getenv("OPEN_ELEVATION_API_KEY", "")