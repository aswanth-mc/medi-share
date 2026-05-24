(function () {
  const modal = document.getElementById("findUnitModal");
  const mapContainer = document.getElementById("unitMap");
  const titleEl = document.getElementById("findUnitModalLabel");
  const locationEl = document.getElementById("findUnitLocation");

  if (!modal || !mapContainer) {
    return;
  }

  let map = null;
  let marker = null;

  function resetMap() {
    if (map) {
      map.remove();
      map = null;
      marker = null;
    }
    mapContainer.innerHTML = "";
  }

  function showMap(lat, lng) {
    resetMap();

    map = L.map(mapContainer).setView([lat, lng], 14);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors",
    }).addTo(map);

    marker = L.marker([lat, lng]).addTo(map);

    setTimeout(function () {
      map.invalidateSize();
    }, 200);
  }

  document.querySelectorAll(".find-unit-btn").forEach(function (button) {
    button.addEventListener("click", function () {
      const unitName = button.dataset.unitName || "Palliative Unit";
      const unitLocation = button.dataset.unitLocation || "Location not available";
      const lat = parseFloat(button.dataset.unitLat);
      const lng = parseFloat(button.dataset.unitLng);

      titleEl.textContent = unitName;
      locationEl.textContent = unitLocation;

      if (Number.isFinite(lat) && Number.isFinite(lng)) {
        showMap(lat, lng);
      } else {
        resetMap();
        mapContainer.innerHTML =
          '<p class="form-help" style="padding: 1rem;">Map location is not available for this unit.</p>';
      }
    });
  });

  modal.addEventListener("hidden.bs.modal", resetMap);
})();
