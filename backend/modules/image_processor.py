import cv2
import numpy as np
from PIL import Image
import io

async def process_image(image_bytes):
    # Convert bytes to numpy array
    img = Image.open(io.BytesIO(image_bytes))
    img = np.array(img.convert('RGB'))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Dominant color ratios (green, blue, other)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Green: hue ~ 40-80, saturation > 50
    green_mask = cv2.inRange(hsv, (40, 50, 20), (80, 255, 255))
    green_ratio = np.sum(green_mask > 0) / (img.shape[0] * img.shape[1])

    # Blue: hue ~ 100-130
    blue_mask = cv2.inRange(hsv, (100, 50, 20), (130, 255, 255))
    blue_ratio = np.sum(blue_mask > 0) / (img.shape[0] * img.shape[1])

    # Edge detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_ratio = np.sum(edges > 0) / (img.shape[0] * img.shape[1])
    has_edges = edge_ratio > 0.05

    # Simple texture: variance of gray
    texture = np.var(gray)
    environment = "urban" if has_edges and texture > 1000 else "natural"

    return {
        "green_ratio": float(green_ratio),
        "blue_ratio": float(blue_ratio),
        "has_edges": has_edges,
        "environment": environment,
        "edge_ratio": float(edge_ratio)
    }