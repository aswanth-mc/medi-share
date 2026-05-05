function openModal(id) {
    document.getElementById("modal-" + id).style.display = "block";
}

function closeModal(id) {
    document.getElementById("modal-" + id).style.display = "none";
}

// Close modal when clicking outside
window.onclick = function(event) {
    document.querySelectorAll('.modal').forEach(modal => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
};