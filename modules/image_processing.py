import cv2
import numpy as np
import os
from google.cloud import vision
from google.oauth2 import service_account

def process_image(img_bgr):
    """Extract labels using Google Vision (optional) and compute simple OpenCV features."""
    labels = []
    # Use Google Vision if API key is set
    vision_key = os.getenv("GOOGLE_VISION_API_KEY")
    if vision_key:
        # For simplicity, we assume the key is set as an environment variable
        # In production, you'd create a client with credentials
        try:
            client = vision.ImageAnnotatorClient()
            # Convert BGR to RGB and encode as JPEG
            _, encoded = cv2.imencode('.jpg', cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
            image = vision.Image(content=encoded.tobytes())
            response = client.label_detection(image=image)
            labels = [label.description for label in response.label_annotations]
        except Exception:
            pass

    # OpenCV: compute color histogram, edge density, etc.
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edge_density = np.sum(edges > 0) / edges.size

    # Dominant colors (simplified: use mean of HSV)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    hue_mean = np.mean(hsv[:,:,0])

    # For demonstration, we return a dictionary of features
    features = {
        "edge_density": edge_density,
        "hue_mean": hue_mean,
        "labels": labels
    }
    return labels, features