function openModal(id) {
    document.getElementById("modal-" + id).classList.add("show");
}

function closeModal(id) {
    document.getElementById("modal-" + id).classList.remove("show");
}

window.onclick = function(event) {
    document.querySelectorAll('.modal').forEach(modal => {
        if (event.target === modal) {
            modal.classList.remove("show");
        }
    });
};