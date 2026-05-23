const map = L.map('map').setView([11.2588, 75.7804], 13);

L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
        attribution: '&copy; OpenStreetMap contributors'
    }
).addTo(map);

let marker;

map.on('click', async function(e) {

    const lat = e.latlng.lat;

    const lng = e.latlng.lng;

    document.getElementById('latitude').value = lat;

    document.getElementById('longitude').value = lng;

    if (marker) {

        map.removeLayer(marker);

    }

    marker = L.marker([lat, lng]).addTo(map);

    const response = await fetch(
        `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
    );

    const data = await response.json();

    document.getElementById('location_name').value =
        data.display_name;

});
