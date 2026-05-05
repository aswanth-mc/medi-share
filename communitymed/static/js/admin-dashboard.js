function openModal(id) {
    const modal = document.getElementById("modal-" + id);
    if (modal) {
        modal.classList.add("show");
    }
}

function closeModal(id) {
    const modal = document.getElementById("modal-" + id);
    if (modal) {
        modal.classList.remove("show");
    }
}

// Close modal if user clicks anywhere outside of the white box
window.onclick = function(event) {
    if (event.target.classList.contains('modal-bg')) {
        event.target.classList.remove("show");
    }
};