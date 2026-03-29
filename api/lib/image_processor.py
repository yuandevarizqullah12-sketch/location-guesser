from PIL import Image, ImageFilter
import numpy as np
import io

async def process_image(image_bytes):
    """
    Ekstrak fitur dari gambar: dominan warna, edge, tekstur.
    Menggunakan PIL saja, tanpa OpenCV.
    """
    # Load image dengan PIL
    img = Image.open(io.BytesIO(image_bytes))
    
    # Resize jika terlalu besar untuk performa
    max_size = 1024
    if max(img.size) > max_size:
        ratio = max_size / max(img.size)
        new_size = tuple(int(dim * ratio) for dim in img.size)
        img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Convert ke RGB jika perlu
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Konversi ke numpy array untuk analisis
    pixels = np.array(img)
    
    # Dominant color (green, blue, other)
    # Green ratio: pixel dimana green > red AND green > blue
    green_mask = (pixels[:,:,1] > pixels[:,:,0]) & (pixels[:,:,1] > pixels[:,:,2])
    green_ratio = np.mean(green_mask)
    
    # Blue ratio: pixel dimana blue > red AND blue > green
    blue_mask = (pixels[:,:,2] > pixels[:,:,0]) & (pixels[:,:,2] > pixels[:,:,1])
    blue_ratio = np.mean(blue_mask)
    
    # Edge detection menggunakan PIL
    edges = img.filter(ImageFilter.FIND_EDGES)
    edge_pixels = np.array(edges.convert('L'))
    edge_ratio = np.mean(edge_pixels > 50)
    has_edges = edge_ratio > 0.05
    
    # Texture: variance of grayscale
    gray = img.convert('L')
    gray_array = np.array(gray)
    texture = np.var(gray_array)
    
    # Environment classification
    environment = "urban" if has_edges and texture > 1000 else "natural"
    
    return {
        "green_ratio": float(green_ratio),
        "blue_ratio": float(blue_ratio),
        "has_edges": has_edges,
        "environment": environment,
        "edge_ratio": float(edge_ratio),
        "texture": float(texture)
    }