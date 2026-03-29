const form = document.getElementById('uploadForm');
const loadingDiv = document.getElementById('loading');
const resultsDiv = document.getElementById('results');
const cardsContainer = document.getElementById('cards');
let map = null;
let markers = [];

// Deteksi environment (local atau production)
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api/analyze'
    : '/api/analyze';

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const imageFile = document.getElementById('image').files[0];
    const clue = document.getElementById('clue').value;

    if (!imageFile) {
        alert('Harap pilih gambar terlebih dahulu');
        return;
    }

    const formData = new FormData();
    formData.append('image', imageFile);
    if (clue) formData.append('clue', clue);

    loadingDiv.style.display = 'block';
    resultsDiv.style.display = 'none';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });
        
        // Cek apakah response OK
        if (!response.ok) {
            const text = await response.text();
            console.error('Server response:', text);
            throw new Error(`HTTP ${response.status}: ${text.substring(0, 100)}`);
        }
        
        // Parse JSON
        const data = await response.json();
        
        if (data.error) {
            alert('Error: ' + data.error);
            loadingDiv.style.display = 'none';
            return;
        }
        
        if (!data.results || data.results.length === 0) {
            alert('Tidak ada lokasi yang ditemukan. Coba upload gambar lain.');
            loadingDiv.style.display = 'none';
            return;
        }

        displayResults(data.results);
        loadingDiv.style.display = 'none';
        resultsDiv.style.display = 'block';
    } catch (err) {
        console.error('Fetch error:', err);
        alert('Gagal menghubungi server: ' + err.message);
        loadingDiv.style.display = 'none';
    }
});

function displayResults(locations) {
    cardsContainer.innerHTML = '';
    if (map) {
        map.remove();
        map = null;
    }

    map = L.map('map').setView([0, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> contributors'
    }).addTo(map);

    markers.forEach(m => map.removeLayer(m));
    markers = [];

    locations.forEach((loc, idx) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <h3>${idx+1}. ${loc.name || 'Lokasi Tidak Bernama'}</h3>
            <div class="score">${loc.confidence}%</div>
            <div class="coords">📍 ${loc.lat.toFixed(5)}, ${loc.lon.toFixed(5)}</div>
            <div>🎯 Skor: ${loc.total_score}/110</div>
        `;
        cardsContainer.appendChild(card);

        const marker = L.marker([loc.lat, loc.lon])
            .bindPopup(`
                <b>${loc.name || 'Lokasi'}</b><br>
                Confidence: ${loc.confidence}%<br>
                Skor: ${loc.total_score}/110
            `)
            .addTo(map);
        markers.push(marker);
    });

    if (locations.length > 0) {
        const bounds = L.latLngBounds(markers.map(m => m.getLatLng()));
        map.fitBounds(bounds);
    }
}