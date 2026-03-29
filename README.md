# 🌍 GeoGuessr - Rule-Based Location Guesser

Sistem tebak lokasi dari gambar menggunakan **non-AI**, **rule-based logic**, dan **5 data sources** multi-layer.

## ✨ Fitur

- 🖼️ **Image Processing**: Deteksi warna dominan, edge, dan tekstur
- 🌍 **Geo Map Module**: OSM (jalan/sungai), Topo (gunung/elevasi), Esri (satellite)
- 📸 **Image Database**: Mapillary (street-level), OpenAerialMap (aerial)
- 💡 **Clue Module**: Filter berdasarkan kota/negara
- 🧾 **Metadata Module**: Ekstrak GPS dari EXIF
- 🧠 **Coordinator**: Scoring system multi-layer
- 🗺️ **Map Preview**: Leaflet + OSM
- ⚡ **Optimasi**: Caching, parallel requests, bounding box

## 🛠️ Tech Stack

**Backend:**
- FastAPI
- OpenCV (image processing)
- aiohttp (async API calls)
- geopy (geocoding)

**Frontend:**
- HTML5/CSS3
- JavaScript (Fetch API)
- Leaflet.js

## 📦 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/USERNAME/geolocation-guesser.git
cd geolocation-guesser