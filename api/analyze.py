import os
import asyncio
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from lib.image_processor import process_image
from lib.geo_map import get_candidates
from lib.image_db import validate_with_images
from lib.clue import process_clue
from lib.metadata import extract_metadata
from lib.coordinator import rank_locations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Location Guesser API is running", "status": "active"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/analyze")
async def analyze(
    image: UploadFile = File(...),
    clue: Optional[str] = Form(None)
):
    try:
        contents = await image.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Empty image")

        # Limit file size to 4.5MB (Vercel limit)
        if len(contents) > 4.5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large. Max 4.5MB")

        # Image processing module
        img_features = await process_image(contents)

        # Metadata module
        metadata = await extract_metadata(contents)

        # Clue module
        clue_info = await process_clue(clue)

        # Geo map module
        candidates = await get_candidates(img_features, clue_info, metadata)
        if not candidates:
            return JSONResponse(
                content={"error": "No candidates found based on image and clue."},
                status_code=404
            )

        # Image database module
        candidates = await validate_with_images(candidates, img_features)

        # Coordinator
        top5 = rank_locations(candidates, img_features, clue_info, metadata)

        return {"results": top5}

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

# Vercel handler
handler = app