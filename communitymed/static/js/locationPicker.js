const map = L.map('map').setView([11.2588, 75.7804], 10);

// OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let marker;

// Click on map
map.on('click', async function(e) {

    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    // Remove old marker
    if (marker) {
        map.removeLayer(marker);
    }

    // Add new marker
    marker = L.marker([lat, lng]).addTo(map);

    // Set hidden inputs
    document.getElementById('latitude').value = lat;
    document.getElementById('longitude').value = lng;

    // Reverse geocoding
    const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
    );

    const data = await response.json();

    const place = data.display_name;

    document.getElementById('location_name').value = place;
});