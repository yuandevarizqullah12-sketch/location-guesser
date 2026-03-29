import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
from modules.image_processor import process_image
from modules.geo_map import get_candidates
from modules.image_db import validate_with_images
from modules.clue import process_clue
from modules.metadata import extract_metadata
from modules.coordinator import rank_locations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(
    image: UploadFile = File(...),
    clue: str = Form(None)
):
    try:
        # 1. Read image
        contents = await image.read()
        if not contents:
            raise HTTPException(status_code=400, detail="Empty image")

        # 2. Image Processing Module
        img_features = await process_image(contents)

        # 3. Metadata Module
        metadata = await extract_metadata(contents)

        # 4. Clue Module
        clue_info = await process_clue(clue)

        # 5. Geo Map Module (initial candidates)
        candidates = await get_candidates(img_features, clue_info, metadata)

        if not candidates:
            return JSONResponse(
                content={"error": "No candidates found based on image and clue."},
                status_code=404
            )

        # 6. Image Database Module (enrich candidates)
        candidates = await validate_with_images(candidates, img_features)

        # 7. Coordinator
        top5 = rank_locations(candidates, img_features, clue_info, metadata)

        return {"results": top5}

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )