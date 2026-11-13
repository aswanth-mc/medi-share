// Ensure default Leaflet marker assets load properly
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

// Initialize Map
const map = L.map('map').setView([11.2588, 75.7804], 10);

// Use OSM France tile layer
L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
    maxZoom: 20,
    attribution: '&copy; OpenStreetMap France | &copy; OpenStreetMap contributors'
}).addTo(map);

let marker;

// Click event
map.on('click', async function (e) {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    // Remove existing marker if any
    if (marker) {
        map.removeLayer(marker);
    }

    // Place new marker immediately
    marker = L.marker([lat, lng]).addTo(map);

    // Update coordinates in inputs (if they exist in your HTML)
    const latInput = document.getElementById('latitude');
    const lngInput = document.getElementById('longitude');
    const locInput = document.getElementById('location_name');

    if (latInput) latInput.value = lat;
    if (lngInput) lngInput.value = lng;
    if (locInput) locInput.value = 'Fetching address...';

    // Reverse geocode with User-Agent header (required by Nominatim)
    try {
        const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`,
            {
                headers: {
                    'Accept': 'application/json'
                }
            }
        );

        if (!response.ok) throw new Error('Geocoding request failed');
        const data = await response.json();

        if (locInput) {
            locInput.value = data.display_name || `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
        }
    } catch (err) {
        console.warn('Could not retrieve address:', err);
        if (locInput) {
            locInput.value = `${lat.toFixed(5)}, ${lng.toFixed(5)}`;
        }
    }
});