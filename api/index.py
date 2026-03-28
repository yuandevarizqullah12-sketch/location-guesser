import os
import io
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import numpy as np
import cv2

from modules.metadata import extract_gps
from modules.clue import geocode_clue
from modules.api_sources import search_google_places, search_osm, search_wikidata
from modules.image_processing import process_image
from modules.coordinator import Coordinator
from modules.llama_assistant import LlamaAssistant

app = FastAPI()

# Mount static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Location Guesser API is running"}

@app.post("/guess")
async def guess_location(
    image: UploadFile = File(...),
    clue: str = Form(None)
):
    # 1. Read and validate image
    try:
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents)).convert("RGB")
        # Convert to OpenCV format
        img_array = np.array(pil_image)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # 2. Extract metadata (EXIF GPS)
    gps_coords = extract_gps(contents)

    # 3. Process image (OpenCV features + Google Vision labels)
    image_labels, image_features = process_image(img_bgr)

    # 4. Geocode clue if provided
    clue_location = None
    if clue:
        clue_location = geocode_clue(clue)

    # 5. Query external APIs for candidate locations
    candidates = []
    # Use Google Places (primary)
    if os.getenv("GOOGLE_MAPS_API_KEY"):
        google_candidates = await search_google_places(clue or gps_coords, gps_coords)
        candidates.extend(google_candidates)
    # Use OSM as secondary
    osm_candidates = await search_osm(clue or gps_coords)
    candidates.extend(osm_candidates)

    # Remove duplicates (by place_id or coordinates)
    unique = {}
    for cand in candidates:
        key = cand.get("place_id") or f"{cand['lat']:.4f},{cand['lng']:.4f}"
        if key not in unique:
            unique[key] = cand
    candidates = list(unique.values())

    # 6. Optional: LLaMA interpretation of clue
    llama_suggestions = None
    if clue and os.getenv("LLAMA_API_KEY"):
        llama = LlamaAssistant()
        llama_suggestions = llama.interpret_clue(clue)

    # 7. Coordinator: combine all scores and rank top 5
    coordinator = Coordinator()
    top_5 = coordinator.rank(
        candidates,
        image_labels=image_labels,
        clue_text=clue,
        clue_location=clue_location,
        gps=gps_coords,
        llama_suggestions=llama_suggestions
    )

    return JSONResponse(content={"top_5": top_5})